package research;

import java.io.BufferedWriter;
import java.lang.reflect.Array;
import java.lang.reflect.Field;
import java.lang.reflect.Proxy;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.Map;
import java.util.Queue;
import java.util.TreeSet;
import java.util.Set;
import java.util.TreeMap;
import net.fabricmc.api.ClientModInitializer;

/** Read engine outputs after resources have finished loading in the real client. */
public final class ComparisonProbe implements ClientModInitializer {
    @Override public void onInitializeClient() {
        try {
            String holder="net.fabricmc.fabric.api.client.event.lifecycle.v1.ClientTickEvents";
            Class<?> listener=Class.forName(holder+"$EndTick");
            Object event=Class.forName(holder).getField("END_CLIENT_TICK").get(null);
            Object callback=Proxy.newProxyInstance(listener.getClassLoader(),new Class<?>[]{listener},
               (self,method,args)->{
                   if (!method.getName().equals("onEndTick")) return null;
                   try {
                       if (recorded) return null;
                       if (Boolean.getBoolean("research.exposure") &&
                           (member(args[0],"310","field_1687")==null || member(args[0],"310","field_1724")==null))
                           return null;
                       if ((boolean) call(args[0],"310","method_53466")) {
                           new ComparisonProbe().run(args[0]);
                           if (!Boolean.getBoolean("research.keep_open")) System.exit(0);
                           else return null;
                       }
                   } catch (Exception error) {
                       error.printStackTrace();
                       System.exit(1);
                   }
                   return null;
               });
            Class.forName("net.fabricmc.fabric.api.event.Event").getMethod("register",Object.class)
                .invoke(event,callback);
        } catch (Exception error) {
            throw new IllegalStateException("Cannot register comparison probe",error);
        }
    }

    // 1.21.1 and 1.21.11 use the Fabric intermediary names for their respective engine methods.
    private static final Class<?>[] NONE={};
    private static Class<?> mc(String id) throws ReflectiveOperationException {
        return Class.forName("net.minecraft.class_"+id);
    }
    private static Object member(Object receiver, String owner, String name) throws Exception {
        Field f=mc(owner).getDeclaredField(name);
        f.setAccessible(true);
        return f.get(receiver);
    }
    private static Object call(Object receiver,String owner,String method) throws Exception {
        return call(receiver,owner,method,NONE);
    }
    private static Object call(Object receiver,String owner,String method,Class<?>[] types,Object... args) throws Exception {
        return mc(owner).getMethod(method,types).invoke(receiver,args);
    }
    private static Object key(String id) throws Exception {
        return call(null,"2960","method_60654",new Class<?>[]{String.class},id);
    }
    private Object registryGet(Object registry,Object key) throws Exception {
        return call(registry,"2378",older?"method_10223":"method_63535",new Class<?>[]{mc("2960")},key);
    }

    private boolean older;
    private Object client, blocks, items, air, stone, pos, empty, modelManager;
    private Object[] directions;
    private BufferedWriter out;
    private Class<?> vectorType;
    private static boolean recorded;

    private void run(Object game) throws Exception {
        if (recorded) return;
        recorded=true;
        client=game;
        older=System.getProperty("research.mc").equals("1.21.1");
        blocks=member(null,"7923","field_41175");
        items=member(null,"7923","field_41178");
        air=defaultState("minecraft:air");
        stone=defaultState("minecraft:stone");
        pos=member(null,"2338","field_10980");
        empty=member(null,"2682","field_12294");
        directions=mc("2350").getEnumConstants();
        modelManager=call(game,"310","method_1541");
        vectorType=Class.forName("org.joml.Vector3fc");
        try (BufferedWriter target=Files.newBufferedWriter(Path.of(System.getProperty("research.output")))) {
            out=target;
            write("kind","case","key","value");
            List<String> input=Files.readAllLines(Path.of(System.getProperty("research.targets")));
            if (Boolean.getBoolean("research.exposure")) {
                auditExposure(input);
                return;
            }
            for (String line:input) {
                String[] values=line.split("\t",-1);
                switch(values[0]) {
                    case "BLOCK" -> inspectBlock(values[1],values[2],values[3]);
                    case "ITEM" -> inspectItem(values[1],values[2]);
                    case "SPRITE" -> inspectSprite(values[1],values[2]);
                    default -> throw new IllegalArgumentException(line);
                }
            }
            if (!older) inspectBed();
        }
    }

    private void auditExposure(List<String> requests) throws Exception {
        Set<String> wanted=new TreeSet<>();
        for (String request:requests) {
            String[] columns=request.split("\\t",-1);
            if (columns[0].equals("SPRITE")) wanted.add(columns[2]);
        }
        Object world=member(client,"310","field_1687");
        Object player=member(client,"310","field_1724");
        Object source=call(player,"1297","method_24515");
        Object manager=member(client,"310","field_1713");
        Queue<?> newParticles=(Queue<?>) member(manager,"702","field_3836");

        int blockCount=0, stateCount=0;
        Map<String,Set<String>> representatives=new TreeMap<>();
        for (Object id:registryIds(blocks)) {
            blockCount++;
            Object block=registryGet(blocks,id);
            Object states=call(block,"2248","method_9595");
            Map<String,Object> selected=new TreeMap<>();
            int count=0;
            for (Object state:(Iterable<?>)call(states,"2689","method_11662")) {
                count++;
                if (!(boolean)call(state,"4970$class_4971","method_45475")) continue;
                Object model=call(modelManager,"776","method_3349",new Class<?>[]{mc("2680")},state);
                String sprite=spriteId(call(model,"1087",older?"method_4711":"method_68511"));
                if (wanted.contains(sprite)) selected.putIfAbsent(sprite,state);
            }
            stateCount+=count;
            write("BLOCK_SCAN",id.toString(),"state_count",Integer.toString(count));
            for (var entry:selected.entrySet()) {
                String texture=entry.getKey();
                Object state=entry.getValue();
                write("PARTICLE_MODEL",texture,id.toString(),packed(properties(state)));
                Set<String> namespaceHits=representatives.computeIfAbsent(texture,k->new TreeSet<>());
                String namespace=id.toString().split(":",2)[0];
                if (namespaceHits.contains(namespace)) continue;
                int previous=newParticles.size();
                call(world,"1937","method_31595",new Class<?>[]{mc("2338"),mc("2680")},source,state);
                Set<String> observed=new TreeSet<>();
                int index=0, generated=0;
                for (Object particle:newParticles) {
                    if (index++<previous || !mc("727").isInstance(particle)) continue;
                    Object sprite=member(particle,older?"4003":"3940",older?"field_17886":"field_62632");
                    observed.add(spriteId(sprite));
                    generated++;
                }
                write("PARTICLE_EVENT",texture,id.toString(),generated+"|"+String.join(";",observed));
                if (observed.contains(texture)) namespaceHits.add(namespace);
            }
        }
        int itemCount=0;
        Object renderer=older?call(client,"310","method_1480"):call(client,"310","method_65386");
        Object mode=member(null,"811","field_4317");
        for (Object id:registryIds(items)) {
            itemCount++;
            Object item=registryGet(items,id);
            Object stack=mc("1799").getConstructor(mc("1935")).newInstance(item);
            Set<String> visible=new TreeSet<>();
            List<String> special=new ArrayList<>();
            if (older) {
                Object model=call(renderer,"918","method_4019",
                    new Class<?>[]{mc("1799"),mc("1937"),mc("1309"),int.class},stack,world,player,0);
                if ((boolean)call(model,"1087","method_4713")) special.add(model.getClass().getName());
                for (Object side:directions) collectSprites(quads(model,null,side),visible);
                collectSprites(quads(model,null,null),visible);
            } else {
                Object layers=mc("10444").getConstructor().newInstance();
                call(renderer,"10442","method_65598",
                    new Class<?>[]{mc("10444"),mc("1799"),mc("811"),mc("1937"),mc("11566"),int.class},
                    layers,stack,mode,world,player,0);
                Object array=member(layers,"10444","field_55340");
                int count=(int)member(layers,"10444","field_55339");
                for (int i=0;i<count;i++) {
                    Object layer=Array.get(array,i);
                    Object type=member(layer,"10444$class_10446","field_55350");
                    if (type!=null) special.add(type.getClass().getName());
                    collectSprites((List<?>)call(layer,"10444$class_10446","method_67997"),visible);
                }
            }
            write("ITEM_SCAN",id.toString(),"model",String.join(";",visible)+"|"+String.join(";",special));
        }
        write("TOTAL","blocks","count",Integer.toString(blockCount));
        write("TOTAL","states","count",Integer.toString(stateCount));
        write("TOTAL","items","count",Integer.toString(itemCount));
    }

    private List<?> registryIds(Object registry) throws Exception {
        return ((Set<?>)call(registry,"2378","method_10235")).stream()
            .sorted(Comparator.comparing(Object::toString)).toList();
    }

    private void collectSprites(List<?> quads, Set<String> visible) throws Exception {
        for (Object quad:quads) visible.add(spriteId(call(quad,"777",older?"method_35788":"comp_3724")));
    }

    private Object defaultState(String id) throws Exception {
        return call(registryGet(blocks,key(id)),"2248","method_9564");
    }
    private static String packed(Map<String,String> properties) {
        return properties.entrySet().stream().map(e->e.getKey()+"="+e.getValue())
            .collect(java.util.stream.Collectors.joining(";"));
    }
    private Map<String,String> properties(Object state) throws Exception {
        Map<String,String> result=new TreeMap<>();
        for (Map.Entry<?,?> entry:((Map<?,?>) call(state,"2688","method_11656")).entrySet()) {
            String name=(String) call(entry.getKey(),"2769","method_11899");
            String value=(String) call(entry.getKey(),"2769","method_11901",
                new Class<?>[]{Comparable.class},entry.getValue());
            result.put(name,value);
        }
        return result;
    }
    private Object select(Object block,String required) throws Exception {
        Map<String,String> wanted=new TreeMap<>();
        for (String property:required.split(";")) {
            if (!property.isEmpty()) {
                String[] pair=property.split("=",2);
                wanted.put(pair[0],pair[1]);
            }
        }
        Map<String,String> defaults=properties(call(block,"2248","method_9564"));
        Object selected=null;
        int best=Integer.MAX_VALUE;
        for (Object state:(Iterable<?>) call(call(block,"2248","method_9595"),"2689","method_11662")) {
            Map<String,String> trial=properties(state);
            if (!trial.entrySet().containsAll(wanted.entrySet())) continue;
            int dist=(int) trial.entrySet().stream().filter(e->!e.getValue().equals(defaults.get(e.getKey()))).count();
            if (dist<best) {
                best=dist;
                selected=state;
            }
        }
        if (selected==null) throw new IllegalArgumentException("No state for "+required);
        return selected;
    }
    private boolean registered(Object registry,Object id) throws Exception {
        return ((Set<?>) call(registry,"2378","method_10235")).contains(id);
    }
    private void inspectBlock(String label,String blockId,String required) throws Exception {
        Object id=key(blockId);
        if (!registered(blocks,id)) {
            write("BLOCK",label,"registry","NOT_REGISTERED");
            return;
        }
        Object state=select(registryGet(blocks,id),required);
        write("BLOCK",label,"registry",blockId);
        write("BLOCK",label,"properties",packed(properties(state)));
        write("BLOCK",label,"emission",call(state,"4970$class_4971","method_26213").toString());
        for (String kind:List.of("collision","outline")) {
            Object shape=call(state,"4970$class_4971",kind.equals("collision")?"method_26220":"method_26218",
                new Class<?>[]{mc("1922"),mc("2338")},empty,pos);
            write("BLOCK",label,kind,boxes(shape));
        }
        Object model=call(modelManager,"776","method_3349",new Class<?>[]{mc("2680")},state);
        Object particle=call(model,"1087",older?"method_4711":"method_68511");
        write("BLOCK",label,"particle",spriteId(particle));
        inspectQuads(label,model,state);
        for (Object side:directions) {
            write("CULL",label,side.toString(),"air="+draw(state,air,side)+";stone="+draw(state,stone,side));
        }
    }

    private boolean draw(Object state,Object neighbor,Object side) throws Exception {
        if (!older) return (boolean) call(null,"2248","method_9607",
            new Class<?>[]{mc("2680"),mc("2680"),mc("2350")},state,neighbor,side);
        Object offset=call(pos,"2338","method_10093",new Class<?>[]{mc("2350")},side);
        Class<?> view=mc("1922");
        Object simulated=Proxy.newProxyInstance(view.getClassLoader(),new Class<?>[]{view},
             (self,method,args)->method.getName().equals("method_8320")
                 ? (offset.equals(args[0])?neighbor:state):method.invoke(empty,args));
        return (boolean) call(null,"2248","method_9607",
            new Class<?>[]{mc("2680"),view,mc("2338"),mc("2350"),mc("2338")},
            state,simulated,pos,side,offset);
    }

    private List<?> quads(Object model,Object state,Object direction) throws Exception {
        Object random=call(null,"5819","method_43049",new Class<?>[]{long.class},0L);
        if (older) return (List<?>) call(model,"1087","method_4707",
                    new Class<?>[]{mc("2680"),mc("2350"),mc("5819")},state,direction,random);
        List<Object> parts=new ArrayList<>();
        call(model,"1087","method_68513",new Class<?>[]{mc("5819"),List.class},random,parts);
        List<Object> quads=new ArrayList<>();
        for (Object part:parts) quads.addAll((List<?>) call(part,"10889","method_68509",new Class<?>[]{mc("2350")},direction));
        return quads;
    }
    private String spriteId(Object sprite) throws Exception {
        return member(call(sprite,"1058","method_45851"),"7764","field_40536").toString();
    }
    private String frames(Object sprite) throws Exception {
        Object contents=call(sprite,"1058","method_45851");
        Object animation=member(contents,"7764","field_40541");
        return animation==null?"1":Integer.toString(((List<?>)member(animation,"7764$class_5790","field_28472")).size());
    }
    private static String vector(float... values) {
        List<String> words=new ArrayList<>();
        for(float value:values) words.add(Float.toString(value==0f?0f:value));
        return String.join(",",words);
    }
    private float component(Object vec,String axis) throws Exception {
        return (float) vectorType.getMethod(axis).invoke(vec);
    }
    private void inspectQuads(String label,Object model,Object state) throws Exception {
        for(int d=-1;d<directions.length;d++) {
            Object side=d<0?null:directions[d];
            int index=0;
            for(Object quad:quads(model,state,side)) {
                Object sprite=call(quad,"777",older?"method_35788":"comp_3724");
                String face=call(quad,"777",older?"method_3358":"comp_3723").toString();
                String tint=call(quad,"777",older?"method_3359":"comp_3722").toString();
                float u0=(float)call(sprite,"1058","method_4594"),u1=(float)call(sprite,"1058","method_4577");
                float v0=(float)call(sprite,"1058","method_4593"),v1=(float)call(sprite,"1058","method_4575");
                List<String> vertices=new ArrayList<>();
                if (older) {
                    int[] data=(int[])call(quad,"777","method_3357");
                    if (data.length!=32) throw new IllegalStateException("Unexpected vertex format: "+data.length);
                    for(int i=0;i<32;i+=8) {
                        float u=Float.intBitsToFloat(data[i+4]),v=Float.intBitsToFloat(data[i+5]);
                        vertices.add(vector(Float.intBitsToFloat(data[i]),Float.intBitsToFloat(data[i+1]),
                                            Float.intBitsToFloat(data[i+2]),(u-u0)/(u1-u0),(v-v0)/(v1-v0)));
                    }
                } else {
                    for (int i=0;i<4;i++) {
                        Object p=call(quad,"777","method_76648",new Class<?>[]{int.class},i);
                        long uv=(long)call(quad,"777","method_76649",new Class<?>[]{int.class},i);
                        float u=Float.intBitsToFloat((int)(uv>>>32)),v=Float.intBitsToFloat((int)uv);
                        vertices.add(vector(component(p,"x"),component(p,"y"),component(p,"z"),
                                            (u-u0)/(u1-u0),(v-v0)/(v1-v0)));
                    }
                }
                String data=String.join("|",face,spriteId(sprite),tint,frames(sprite),String.join(";",vertices));
                write("QUAD",label,(side==null?"unculled":side.toString())+"/"+index++,data);
            }
        }
    }

    private String boxes(Object shape) throws Exception {
        List<String> result=new ArrayList<>();
        for (Object bounds:(Iterable<?>)call(shape,"265","method_1090")) {
            List<String> values=new ArrayList<>();
            for(String field:List.of("field_1323","field_1322","field_1321","field_1320","field_1325","field_1324"))
                values.add(member(bounds,"238",field).toString());
            result.add(String.join(",",values));
        }
        result.sort(Comparator.naturalOrder());
        return String.join(";",result);
    }

    private void inspectSprite(String label,String id) throws Exception {
        Object manager=call(client,"310",older?"method_1554":"method_72703");
        Object atlas=call(manager,older?"1092":"11697",older?"method_24153":"method_73025",
                          new Class<?>[]{mc("2960")},older?member(null,"1059","field_5275"):key("minecraft:blocks"));
        Object sprite=call(atlas,"1059","method_4608",new Class<?>[]{mc("2960")},key(id));
        write("SPRITE",label,"id",spriteId(sprite));
        write("SPRITE",label,"frame_count",frames(sprite));
    }

    private void inspectItem(String label,String id) throws Exception {
        Object idKey=key(id);
        if (!registered(items,idKey)) {
            write("ITEM",label,"registry","NOT_REGISTERED");
            return;
        }
        Object item=registryGet(items,idKey);
        write("ITEM",label,"registry",id);
        if (older) {
            Object meshes=call(call(client,"310","method_1480"),"918","method_4012");
            Object model=call(meshes,"763","method_3304",new Class<?>[]{mc("1792")},item);
            write("ITEM",label,"particle",spriteId(call(model,"1087","method_4711")));
            inspectQuads(label,model,null);
        } else {
            Object manager=call(client,"310","method_65386");
            Object renderState=mc("10444").getConstructor().newInstance();
            Object stack=mc("1799").getConstructor(mc("1935")).newInstance(item);
            Object mode=member(null,"811","field_4317");
            call(manager,"10442","method_65598",
                new Class<?>[]{mc("10444"),mc("1799"),mc("811"),mc("1937"),mc("11566"),int.class},
                renderState,stack,mode,null,null,0);
            for (int i=0;i<Array.getLength(member(renderState,"10444","field_55340"));i++) {
                Object layer=Array.get(member(renderState,"10444","field_55340"),i);
                Object special=member(layer,"10444$class_10446","field_55350");
                if(special!=null) write("ITEM",label,"special_"+i,special.getClass().getName());
            }
        }
    }

    private void inspectBed() throws Exception {
        Object north=java.util.Arrays.stream(directions).filter(d->d.toString().equals("north")).findFirst().orElseThrow();
        Object loader=call(client,"310","method_31974");
        for(String name:List.of("foot","head")) {
            Object layer=member(null,"5602",name.equals("foot")?"field_27680":"field_27681");
            Object model=call(loader,"5599","method_32072",new Class<?>[]{mc("5601")},layer);
            Object matrices=mc("4587").getConstructor().newInstance();
            var transform=mc("825").getDeclaredMethod("method_72159",mc("4587"),boolean.class,mc("2350"));
            transform.setAccessible(true);
            transform.invoke(null,matrices,false,north);
            bedBranch(name,"root",model,matrices);
        }
    }

    private void bedBranch(String half,String path,Object part,Object matrices) throws Exception {
        call(matrices,"4587","method_22903");
        call(part,"630","method_22703",new Class<?>[]{mc("4587")},matrices);
        Object matrix=call(call(matrices,"4587","method_23760"),"4587$class_4665","method_23761");
        Class<?> vec=Class.forName("org.joml.Vector3f");
        int boxIndex=0;
        for (Object box:(Iterable<?>)member(part,"630","field_3663")) {
            int faceIndex=0;
            for (Object face:(Object[])member(box,"630$class_628","field_3649")) {
                List<String> vertices=new ArrayList<>();
                for (Object vertex:(Object[])call(face,"630$class_593","comp_3184")) {
                    float x=(float)call(vertex,"630$class_618","method_74250");
                    float y=(float)call(vertex,"630$class_618","method_74251");
                    float z=(float)call(vertex,"630$class_618","method_74252");
                    Object point=vec.getConstructor().newInstance();
                    matrix.getClass().getMethod("transformPosition",float.class,float.class,float.class,vec).invoke(matrix,x,y,z,point);
                    vertices.add(vector(component(point,"x"),component(point,"y"),component(point,"z"),
                        (float)call(vertex,"630$class_618","comp_3187"),(float)call(vertex,"630$class_618","comp_3188")));
                }
                write("BED",half,path+"/"+boxIndex+"/"+faceIndex++,String.join(";",vertices));
            }
            boxIndex++;
        }
        Map<?,?> children=(Map<?,?>)member(part,"630","field_3661");
        for(Object name:children.keySet().stream().sorted(Comparator.comparing(Object::toString)).toList()) {
            bedBranch(half,path+"/"+name,children.get(name),matrices);
        }
        call(matrices,"4587","method_22909");
    }

    private void write(String... columns) throws Exception {
        out.write(String.join("\t",columns));
        out.newLine();
    }
}
