package mcfrprobe;

import java.lang.reflect.*;
import java.util.*;
import org.joml.Matrix4fc;
import org.joml.Vector3f;

// Additional original engine probe: world-piece preparation and sprite ID.
// No rendered game, GPU, original source rewriting, or user interaction.
public class H20BedPoseMaterialProbe extends H20BedMeshProbe {
    static Object invoke(Object obj,String owner,String method,Class<?>[] types,Object... args) throws Exception {
        Method m=cls(owner).getDeclaredMethod(names.getProperty(owner+"."+method),types);
        m.setAccessible(true);
        return m.invoke(obj,args);
    }
    static Object pose() throws Exception {
        return cls("PoseStack").getDeclaredConstructor().newInstance();
    }
    static void visitWorld(String half,String direction,String path,Object p,Object stack) throws Exception {
        call0(stack,"PoseStack","pushPose");
        invoke(p,"ModelPart","translateAndRotate",new Class<?>[]{cls("PoseStack")},stack);
        Matrix4fc matrix=(Matrix4fc)call0(call0(stack,"PoseStack","last"),"Pose","pose");
        List<?> cubes=(List<?>)field(p,"ModelPart","cubes");
        Map<?,?> children=(Map<?,?>)field(p,"ModelPart","children");
        for(int c=0;c<cubes.size();c++){
            Object polygons=field(cubes.get(c),"Cube","polygons");
            for(int f=0;f<Array.getLength(polygons);f++){
                Object vertices=field(Array.get(polygons,f),"Polygon","vertices");
                for(int v=0;v<Array.getLength(vertices);v++){
                    Object vertex=Array.get(vertices,v);
                    float x=((Number)call0(vertex,"Vertex","worldX")).floatValue();
                    float y=((Number)call0(vertex,"Vertex","worldY")).floatValue();
                    float z=((Number)call0(vertex,"Vertex","worldZ")).floatValue();
                    Vector3f xyz=new Vector3f(x,y,z).mulPosition(matrix);
                    System.out.println("WORLD\t"+half+"\t"+direction+"\t"+path+"\t"+c+"\t"+f+"\t"+v+"\t"+vec(xyz));
                }
            }
        }
        for(String child:children.keySet().stream().map(Object::toString).sorted().toList())
            visitWorld(half,direction,path+"/"+child,children.get(child),stack);
        call0(stack,"PoseStack","popPose");
    }
    public static void main(String[] args) throws Exception {
        try(var in=new java.io.FileInputStream(args[0])){names.load(in);}
        for(String half:List.of("head","foot")){
            Object layer=call0(null,"BedRenderer",half.equals("head")?"createHeadLayer":"createFootLayer");
            Object root=call0(layer,"LayerDefinition","bakeRoot");
            for(String direction:List.of("NORTH","EAST","SOUTH","WEST")){
                Object stack=pose();
                Object facing=field(null,"Direction",direction);
                invoke(null,"BedRenderer","preparePose",new Class<?>[]{cls("PoseStack"),boolean.class,cls("Direction")},stack,false,facing);
                visitWorld(half,direction,"root",root,stack);
            }
        }
        System.out.println("H20_WORLD_POSE_COMPLETE");
        // Registry bootstrapping happens only after geometry; original official
        // APIs resolve the DyeColor.WHITE material.
        call0(null,"SharedConstants","tryDetectVersion");
        call0(null,"Bootstrap","bootStrap");
        Object white=field(null,"DyeColor","WHITE");
        Object material=invoke(null,"Sheets","getBedMaterial",new Class<?>[]{cls("DyeColor")},white);
        System.out.println("WHITE_MATERIAL\t"+call0(material,"Material","texture")+"\t"+call0(material,"Material","atlasLocation"));
        System.out.println("H20_MATERIAL_COMPLETE");
    }
}
