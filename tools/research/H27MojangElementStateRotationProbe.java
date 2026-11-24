package mcfr.research;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.lang.reflect.Constructor;
import java.lang.reflect.Field;
import java.lang.reflect.Method;
import java.nio.charset.StandardCharsets;
import java.util.HashMap;
import java.util.Map;

/**
 * Call unmodified Mojang 1.21.11 element and state rotation methods.
 *
 * Source-pinned original classes:
 * Variant.SimpleModelState.asModelState -> ModelState.transformation
 * -> Transformation.getMatrix;
 * BlockElementRotation.SingleAxisRotation -> BlockElementRotation.transform;
 * FaceBakery.rotateVertexBy (original private method, invoked reflectively).
 *
 * Does NOT call FaceBakery.bakeQuad, atlas interpolation or an actual Minecraft
 * render/client F2. All vertex values are before UV lock and baked quad culling.
 *
 * TSV input (15 fields):
 * id, stateY, uvLock, fromX,fromY,fromZ,toX,toY,toZ,
 * rotationAxis|none, rotationAngle, rotationOriginX,Y,Z, rotationRescale.
 *
 * TSV output: "VERTICES", id, 24 floats (8 source corners * xyz in model 0-16 units).
 */
public final class H27MojangElementStateRotationProbe {
    private static final String[] DIRECTIONS = {"x", "y", "z"};

    private static Object originalStaticField(Class<?> owner, String fieldName) throws Exception {
        Field f = owner.getDeclaredField(fieldName);
        f.setAccessible(true);
        Object result = f.get(null);
        if (result == null) {
            throw new AssertionError("Original Mojang static enum/constant field is null");
        }
        return result;
    }

    public static void main(String[] args) throws Exception {
        if (args.length != 16) {
            throw new IllegalArgumentException("H27 expects exactly 16 original mapped args");
        }
        Class<?> bakery = Class.forName(args[0]);
        Class<?> variant = Class.forName(args[2]);
        Class<?> quadrant = Class.forName(args[3]);
        Class<?> modelState = Class.forName(args[4]);
        Class<?> transformation = Class.forName(args[5]);
        Class<?> elementRotation = Class.forName(args[6]);
        Class<?> singleAxis = Class.forName(args[7]);
        Class<?> axis = Class.forName(args[8]);
        Class<?> rotationValue = Class.forName(args[6] + "$b");
        Class<?> vectorInterface = Class.forName("org.joml.Vector3fc");
        Class<?> matrixInterface = Class.forName("org.joml.Matrix4fc");
        Class<?> vector = Class.forName("org.joml.Vector3f");
        Constructor<?> vectorConstructor = vector.getConstructor(
            float.class, float.class, float.class);
        Method[] vectorComponents = new Method[] {
            vector.getMethod("x"), vector.getMethod("y"), vector.getMethod("z"),
        };
        Constructor<?> variantConstructor = variant.getDeclaredConstructor(
            quadrant, quadrant, quadrant, boolean.class);
        variantConstructor.setAccessible(true);
        Constructor<?> singleAxisConstructor = singleAxis.getDeclaredConstructor(
            axis, float.class);
        singleAxisConstructor.setAccessible(true);
        Constructor<?> elementConstructor = elementRotation.getDeclaredConstructor(
            vectorInterface, rotationValue, boolean.class);
        elementConstructor.setAccessible(true);
        Method asState = variant.getDeclaredMethod(args[9]);
        asState.setAccessible(true);
        Method getTransformation = modelState.getDeclaredMethod(args[10]);
        getTransformation.setAccessible(true);
        Method getMatrix = transformation.getDeclaredMethod(args[11]);
        getMatrix.setAccessible(true);
        Method elementTransform = elementRotation.getDeclaredMethod(args[12]);
        elementTransform.setAccessible(true);
        Method rotate = bakery.getDeclaredMethod(
            args[1], vector, vectorInterface, matrixInterface);
        rotate.setAccessible(true);
        String[] qNames = args[13].split(",", -1);
        String[] aNames = args[14].split(",", -1);
        if (qNames.length != 4 || aNames.length != 3) {
            throw new IllegalArgumentException("Original Quadrant/Axis mapped field list changed");
        }
        Object[] quads = new Object[4];
        for (int i = 0; i < quads.length; ++i) {
            quads[i] = originalStaticField(quadrant, qNames[i]);
            if (!quadrant.isInstance(quads[i])) {
                throw new AssertionError("Mojang Quadrant static field changed");
            }
        }
        Map<String, Object> axes = new HashMap<>();
        for (int i = 0; i < DIRECTIONS.length; ++i) {
            Object axisEnum = originalStaticField(axis, aNames[i]);
            if (!axis.isInstance(axisEnum)) {
                throw new AssertionError("Mojang direction Axis static field changed");
            }
            axes.put(DIRECTIONS[i], axisEnum);
        }
        Object blockCenter = originalStaticField(bakery, args[15]);
        if (!vectorInterface.isInstance(blockCenter)) {
            throw new AssertionError("Original FaceBakery BLOCK_MIDDLE is no longer Vector3fc");
        }
        BufferedReader input = new BufferedReader(
            new InputStreamReader(System.in, StandardCharsets.UTF_8));
        String line;
        int elements = 0;
        int elementRotations = 0;
        while ((line = input.readLine()) != null) {
            if (line.isBlank()) continue;
            String[] t = line.split("\t", -1);
            if (t.length != 15 || !t[0].matches("[a-zA-Z0-9_:-]+")) {
                throw new IllegalArgumentException("Invalid original H27 source element TSV");
            }
            String id = t[0];
            int stateY = Integer.parseInt(t[1]);
            if (stateY != 0 && stateY != 90 && stateY != 180 && stateY != 270) {
                throw new IllegalArgumentException("State Y must be original 90-degree Quadrant");
            }
            boolean uvLock = switch (t[2]) {
                case "false" -> false;
                case "true" -> true;
                default -> throw new IllegalArgumentException("Unknown original uvlock");
            };
            float[] pos = new float[6];
            for (int i = 0; i < 6; ++i) {
                pos[i] = Float.parseFloat(t[i + 3]);
                if (!Float.isFinite(pos[i])) throw new IllegalArgumentException("Nonfinite source element");
            }
            String axisName = t[9];
            float angle = Float.parseFloat(t[10]);
            float[] origin = new float[3];
            for (int i = 0; i < 3; ++i) origin[i] = Float.parseFloat(t[11 + i]);
            boolean rescale = switch (t[14]) {
                case "false" -> false;
                case "true" -> true;
                default -> throw new IllegalArgumentException("Unknown original rescale");
            };
            Object variantState = variantConstructor.newInstance(
                quads[0], quads[stateY / 90], quads[0], uvLock);
            Object originalState = asState.invoke(variantState);
            Object originalTransformation = getTransformation.invoke(originalState);
            Object originalStateMatrix = getMatrix.invoke(originalTransformation);
            if (!matrixInterface.isInstance(originalStateMatrix)) {
                throw new AssertionError("Mojang ModelState transformed matrix type drift");
            }
            Object elementMatrix = null;
            Object elementPivot = null;
            if (!"none".equals(axisName)) {
                if (!axes.containsKey(axisName) || !Float.isFinite(angle)) {
                    throw new IllegalArgumentException("Invalid Adorn element rotation");
                }
                Object single = singleAxisConstructor.newInstance(axes.get(axisName), angle);
                Object elementOrigin = vectorConstructor.newInstance(
                    origin[0], origin[1], origin[2]);
                Object originalElement = elementConstructor.newInstance(
                    elementOrigin, single, rescale);
                elementMatrix = elementTransform.invoke(originalElement);
                if (!matrixInterface.isInstance(elementMatrix)) {
                    throw new AssertionError("Mojang BlockElementRotation.transform type drift");
                }
                // Source JSON element rotation origin uses model pixel units.
                elementPivot = vectorConstructor.newInstance(
                    origin[0] / 16f, origin[1] / 16f, origin[2] / 16f);
                ++elementRotations;
            } else if (angle != 0 || rescale) {
                throw new IllegalArgumentException("Nonempty element rotation without axis");
            }
            StringBuilder output = new StringBuilder("VERTICES\t").append(id);
            for (int corner = 0; corner < 8; ++corner) {
                float x = pos[(corner & 1) == 0 ? 0 : 3] / 16f;
                float y = pos[(corner & 2) == 0 ? 1 : 4] / 16f;
                float z = pos[(corner & 4) == 0 ? 2 : 5] / 16f;
                Object vertex = vectorConstructor.newInstance(x, y, z);
                if (elementMatrix != null) {
                    rotate.invoke(null, vertex, elementPivot, elementMatrix);
                }
                rotate.invoke(null, vertex, blockCenter, originalStateMatrix);
                for (Method component : vectorComponents) {
                    float n = ((Number) component.invoke(vertex)).floatValue() * 16f;
                    if (!Float.isFinite(n)) throw new AssertionError("Nonfinite original Mojang vertex");
                    output.append('\t').append(Float.toString(n));
                }
            }
            System.out.println(output);
            ++elements;
        }
        if (elements == 0) throw new AssertionError("No real Adorn elements submitted");
        System.err.println("H27_MOJANG_ORIGINAL_ROTATED_ELEMENTS=" + elements);
        System.err.println("H27_MOJANG_ORIGINAL_ROTATED_SHELF_ELEMENTS=" + elementRotations);
    }
}
