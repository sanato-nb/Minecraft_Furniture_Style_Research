package research;

import java.io.BufferedWriter;
import java.io.IOException;
import java.lang.reflect.Field;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.lang.reflect.Proxy;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.TreeMap;
import net.fabricmc.api.ClientModInitializer;

/** Reads actual registered states and the engine's collision AABBs in an empty context. */
public final class StateProbe implements ClientModInitializer {
    @Override
    public void onInitializeClient() {
        try {
            String events = "net.fabricmc.fabric.api.client.event.lifecycle.v1.ClientLifecycleEvents";
            Class<?> listener = Class.forName(events + "$ClientStarted");
            Object event = Class.forName(events).getField("CLIENT_STARTED").get(null);
            Object callback = Proxy.newProxyInstance(listener.getClassLoader(), new Class<?>[] {listener},
                (self, method, args) -> {
                    try {
                        run();
                        System.exit(0);
                    } catch (Exception error) {
                        error.printStackTrace();
                        System.exit(1);
                    }
                    return null;
                });
            Class.forName("net.fabricmc.fabric.api.event.Event")
                .getMethod("register", Object.class).invoke(event, callback);
        } catch (ReflectiveOperationException error) {
            throw new IllegalStateException("Unable to register the state probe", error);
        }
    }

    private static Class<?> mc(String suffix) throws ClassNotFoundException {
        return Class.forName("net.minecraft.class_" + suffix);
    }

    private static void run() throws ReflectiveOperationException, IOException {
        boolean old = System.getProperty("research.mc").equals("1.21.1");
        Set<String> namespaces = old ? Set.of("another_furniture", "handcrafted") : Set.of("mcwfurnitures");
        Object registry = mc("7923").getField("field_41175").get(null);
        Class<?> registryType = mc("2378");
        Method get = registryType.getMethod(old ? "method_10223" : "method_63535", mc("2960"));
        Set<?> ids = (Set<?>) registryType.getMethod("method_10235").invoke(registry);
        Object world = mc("2682").getField("field_12294").get(null);
        Object position = mc("2338").getField("field_10980").get(null);
        Method stateManager = mc("2248").getMethod("method_9595");
        Method getStates = mc("2689").getMethod("method_11662");
        Method getEntries = mc("2688").getMethod("method_11656");
        Method propertyName = mc("2769").getMethod("method_11899");
        Method valueName = mc("2769").getMethod("method_11901", Comparable.class);
        Method getCollision = mc("4970$class_4971").getMethod("method_26220", mc("1922"), mc("2338"));
        Method getBoxes = mc("265").getMethod("method_1090");
        List<Field> bounds = new ArrayList<>();
        for (String field : List.of("field_1323", "field_1322", "field_1321", "field_1320", "field_1325", "field_1324")) {
            bounds.add(mc("238").getField(field));
        }
        Path target = Path.of(System.getProperty("research.output"));
        try (BufferedWriter writer = Files.newBufferedWriter(target)) {
            writer.write("block\tproperties\tstatus\tboxes\n");
            for (Object id : ids.stream().sorted((a, b) -> a.toString().compareTo(b.toString())).toList()) {
                String name = id.toString();
                if (!namespaces.contains(name.split(":", 2)[0]) && !Set.of("minecraft:air", "minecraft:stone").contains(name)) {
                    continue;
                }
                Object manager = stateManager.invoke(get.invoke(registry, id));
                for (Object state : (Iterable<?>) getStates.invoke(manager)) {
                    Map<String, String> pairs = new TreeMap<>();
                    for (Map.Entry<?, ?> entry : ((Map<?, ?>) getEntries.invoke(state)).entrySet()) {
                        pairs.put((String) propertyName.invoke(entry.getKey()),
                                  (String) valueName.invoke(entry.getKey(), entry.getValue()));
                    }
                    List<String> properties = new ArrayList<>();
                    pairs.forEach((key, value) -> properties.add(key + "=" + value));
                    List<String> boxes = new ArrayList<>();
                    String status = "OK";
                    try {
                        Object shape = getCollision.invoke(state, world, position);
                        for (Object box : (Iterable<?>) getBoxes.invoke(shape)) {
                            List<String> coordinates = new ArrayList<>();
                            for (Field field : bounds) {
                                coordinates.add(Double.toString(field.getDouble(box)));
                            }
                            boxes.add(String.join(",", coordinates));
                        }
                    } catch (InvocationTargetException error) {
                        status = "CONTEXT_ERROR:" + error.getCause().getClass().getSimpleName();
                        boxes.clear();
                    }
                    boxes.sort(String::compareTo);
                    writer.write(name + "\t" + String.join(",", properties) + "\t" + status + "\t" + String.join(";", boxes) + "\n");
                }
            }
        }
        System.out.println("Finished engine-state probe: " + target);
    }
}
