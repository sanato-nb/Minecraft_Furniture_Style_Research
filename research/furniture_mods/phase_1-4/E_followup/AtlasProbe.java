package research;

import java.io.BufferedWriter;
import java.io.IOException;
import java.lang.reflect.Field;
import java.lang.reflect.Method;
import java.lang.reflect.Proxy;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.TreeMap;
import java.util.TreeSet;
import net.fabricmc.api.ClientModInitializer;

/** Reports live sprites only after the 1.21.1 client finishes its initial reload. */
public final class AtlasProbe implements ClientModInitializer {
    @Override
    public void onInitializeClient() {
        try {
            String events = "net.fabricmc.fabric.api.client.event.lifecycle.v1.ClientTickEvents";
            Class<?> listener = Class.forName(events + "$EndTick");
            Object event = Class.forName(events).getField("END_CLIENT_TICK").get(null);
            Method finished = mc("310").getMethod("method_53466");
            Object callback = Proxy.newProxyInstance(listener.getClassLoader(), new Class<?>[]{listener},
                (self, method, args) -> {
                    if (!method.getName().equals("onEndTick")) {
                        return null;
                    }
                    try {
                        if ((Boolean) finished.invoke(args[0])) {
                            new Sample(args[0]).write();
                            System.exit(0);
                        }
                    } catch (Exception error) {
                        error.printStackTrace();
                        System.exit(1);
                    }
                    return null;
                });
            Class.forName("net.fabricmc.fabric.api.event.Event").getMethod("register",Object.class)
                .invoke(event,callback);
        } catch (ReflectiveOperationException error) {
            throw new IllegalStateException("Unable to register the atlas probe",error);
        }
    }

    private static Class<?> mc(String id) throws ClassNotFoundException {
        return Class.forName("net.minecraft.class_" + id);
    }

    private static final class Sample {
        final Object atlas, blocks, items, blockModelManager, itemModels;
        final Method identifier, sprite, contents, stateEntries, stateManager, getStates;
        final Method blockModel, itemModel, particle, getQuads, quadSprite, random, getRegistry;
        final Object[] directions;
        final Field spriteId;

        Sample(Object client) throws ReflectiveOperationException {
            Class<?> identifierType = mc("2960");
            identifier = identifierType.getMethod("method_60654", String.class);
            Object models = mc("310").getMethod("method_1554").invoke(client);
            Object blockAtlasId = mc("1059").getField("field_5275").get(null);
            atlas = mc("1092").getMethod("method_24153",identifierType).invoke(models,blockAtlasId);
            sprite = mc("1059").getMethod("method_4608",identifierType);
            contents = mc("1058").getMethod("method_45851");
            spriteId = mc("7764").getDeclaredField("field_40536");
            spriteId.setAccessible(true);
            blocks = mc("7923").getField("field_41175").get(null);
            items = mc("7923").getField("field_41178").get(null);
            getRegistry = mc("2378").getMethod("method_10223",identifierType);
            blockModelManager = mc("310").getMethod("method_1541").invoke(client);
            blockModel = mc("776").getMethod("method_3349",mc("2680"));
            Object renderer = mc("310").getMethod("method_1480").invoke(client);
            itemModels = mc("918").getMethod("method_4012").invoke(renderer);
            itemModel = mc("763").getMethod("method_3304",mc("1792"));
            stateManager = mc("2248").getMethod("method_9595");
            getStates = mc("2689").getMethod("method_11662");
            stateEntries = mc("2688").getMethod("method_11656");
            particle = mc("1087").getMethod("method_4711");
            getQuads = mc("1087").getMethod("method_4707",mc("2680"),mc("2350"),mc("5819"));
            directions = mc("2350").getEnumConstants();
            quadSprite = mc("777").getMethod("method_35788");
            random = mc("5819").getMethod("method_43049",long.class);
        }

        String id(Object value) throws ReflectiveOperationException {
            return spriteId.get(contents.invoke(value)).toString();
        }

        void write() throws ReflectiveOperationException, IOException {
            Method registryIds = mc("2378").getMethod("method_10235");
            Set<?> blockIds = (Set<?>) registryIds.invoke(blocks);
            Set<?> itemIds = (Set<?>) registryIds.invoke(items);
            Path target = Path.of(System.getProperty("research.output"));
            try (BufferedWriter out = Files.newBufferedWriter(target)) {
                out.write("kind\trequested\tproperties\tstatus\tsprite\tquad_sprites\n");
                for (String line : Files.readAllLines(Path.of(System.getProperty("research.targets")))) {
                    String[] fields = line.split("\t");
                    String kind = fields[0];
                    String request = fields[1];
                    Object key = identifier.invoke(null,request);
                    switch (kind) {
                        case "SPRITE" -> output(out,kind,request,"","LOOKED_UP",id(sprite.invoke(atlas,key)),"");
                        case "BLOCK" -> {
                            if (!blockIds.contains(key)) {
                                output(out,kind,request,"","NOT_REGISTERED","","");
                            } else {
                                Object block = getRegistry.invoke(blocks,key);
                                Object manager = stateManager.invoke(block);
                                for (Object state : (Iterable<?>) getStates.invoke(manager)) {
                                    Object model = blockModel.invoke(blockModelManager,state);
                                    output(out,kind,request,properties(state),"BAKED",id(particle.invoke(model)),sprites(model,state));
                                }
                            }
                        }
                        case "ITEM" -> {
                            if (!itemIds.contains(key)) {
                                output(out,kind,request,"","NOT_REGISTERED","","");
                            } else {
                                Object item = getRegistry.invoke(items,key);
                                Object model = itemModel.invoke(itemModels,item);
                                output(out,kind,request,"","BAKED",id(particle.invoke(model)),sprites(model,null));
                            }
                        }
                        default -> throw new IllegalArgumentException(kind);
                    }
                }
            }
        }

        String properties(Object state) throws ReflectiveOperationException {
            Map<String,String> result = new TreeMap<>();
            Method name = mc("2769").getMethod("method_11899");
            Method value = mc("2769").getMethod("method_11901",Comparable.class);
            for (Map.Entry<?,?> entry : ((Map<?,?>) stateEntries.invoke(state)).entrySet()) {
                result.put((String) name.invoke(entry.getKey()),(String) value.invoke(entry.getKey(),entry.getValue()));
            }
            List<String> labels = new ArrayList<>();
            result.forEach((key,val) -> labels.add(key + "=" + val));
            return String.join(",",labels);
        }

        String sprites(Object model,Object state) throws ReflectiveOperationException {
            Set<String> names = new TreeSet<>();
            for (int i = -1; i < directions.length; i++) {
                Object side = i < 0 ? null : directions[i];
                for (Object quad : (Iterable<?>) getQuads.invoke(model,state,side,random.invoke(null,0L))) {
                    names.add(id(quadSprite.invoke(quad)));
                }
            }
            return String.join("|",names);
        }

        static void output(BufferedWriter out,String... columns) throws IOException {
            out.write(String.join("\t",columns));
            out.newLine();
        }
    }
}
