// H20 isolated official model-layer baking probe (no game, no render context).
// Names supplied from SHA-pinned Mojang mapping. Do not patch original classes.
import java.lang.reflect.*;
import java.util.*;
import org.joml.Vector3fc;

public class H20BedMeshProbe {
    static final Properties names=new Properties();
    static Class<?> cls(String name) throws Exception {
        return Class.forName(names.getProperty(name));
    }
    static Object field(Object obj,String owner,String name) throws Exception {
        Field f=cls(owner).getDeclaredField(names.getProperty(owner+"."+name));
        f.setAccessible(true);
        return f.get(obj);
    }
    static Object call0(Object obj,String owner,String name) throws Exception {
        Method m=cls(owner).getDeclaredMethod(names.getProperty(owner+"."+name));
        m.setAccessible(true);
        return m.invoke(obj);
    }
    static String vec(Vector3fc v) {return v.x()+"\t"+v.y()+"\t"+v.z();}
    static Vector3fc vectorField(Object obj) throws Exception {
        List<Field> fs=Arrays.stream(obj.getClass().getDeclaredFields())
            .filter(f->!Modifier.isStatic(f.getModifiers())&&Vector3fc.class.isAssignableFrom(f.getType())).toList();
        if(fs.size()!=1)throw new IllegalStateException("expected one vector field: "+obj.getClass()+" count "+fs.size());
        fs.get(0).setAccessible(true);
        return (Vector3fc)fs.get(0).get(obj);
    }
    static void visit(String half,String path,Object p) throws Exception {
        String part="ModelPart";
        StringBuilder out=new StringBuilder("PART\t"+half+"\t"+path);
        for(String f:List.of("x","y","z","xRot","yRot","zRot","xScale","yScale","zScale"))
            out.append("\t").append(field(p,part,f));
        List<?> cubes=(List<?>)field(p,part,"cubes");
        Map<?,?> children=(Map<?,?>)field(p,part,"children");
        out.append("\t").append(cubes.size()).append("\t").append(children.size());
        System.out.println(out);
        for(int c=0;c<cubes.size();c++){
            Object cube=cubes.get(c);
            Object polys=field(cube,"Cube","polygons");
            StringBuilder bounds=new StringBuilder("CUBE\t"+half+"\t"+path+"\t"+c);
            for(String f:List.of("minX","minY","minZ","maxX","maxY","maxZ"))
                bounds.append("\t").append(field(cube,"Cube",f));
            bounds.append("\t").append(Array.getLength(polys));
            System.out.println(bounds);
            for(int s=0;s<Array.getLength(polys);s++){
                Object poly=Array.get(polys,s);
                System.out.println("FACE\t"+half+"\t"+path+"\t"+c+"\t"+s+"\t"+vec(vectorField(poly)));
                Object vertices=field(poly,"Polygon","vertices");
                for(int v=0;v<Array.getLength(vertices);v++){
                    Object vertex=Array.get(vertices,v);
                    System.out.println("VERTEX\t"+half+"\t"+path+"\t"+c+"\t"+s+"\t"+v+"\t"+vec(vectorField(vertex))+"\t"+field(vertex,"Vertex","u")+"\t"+field(vertex,"Vertex","v"));
                }
            }
        }
        List<String> keys=children.keySet().stream().map(Object::toString).sorted().toList();
        for(String child:keys)visit(half,path+"/"+child,children.get(child));
    }
    public static void main(String[] args) throws Exception {
        try(var in=new java.io.FileInputStream(args[0])){names.load(in);}
        for(String half:List.of("head","foot")){
            Object layer=call0(null,"BedRenderer",half.equals("head")?"createHeadLayer":"createFootLayer");
            Object root=call0(layer,"LayerDefinition","bakeRoot");
            visit(half,"root",root);
        }
        System.out.println("H20_BAKED_MODEL_FACTORIES_COMPLETE");
    }
}
