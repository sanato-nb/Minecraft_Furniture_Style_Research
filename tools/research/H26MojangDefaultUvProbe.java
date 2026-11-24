package mcfr.research;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.lang.reflect.Constructor;
import java.lang.reflect.Method;
import java.nio.charset.StandardCharsets;
import java.util.HashMap;
import java.util.Map;

/**
 * H26 — invoke the UNMODIFIED, obfuscated official Mojang FaceBakery.defaultFaceUV.
 * All mapped class/method/enum names are provided by the source SHA-pinned Python
 * mapping validator; this helper contains no duplicated/reimplemented UV formula.
 * It does not bake a full quad or render a Minecraft client frame.
 *
 * Input TSV: face_id, direction, from_x, from_y, from_z, to_x, to_y, to_z.
 * Output TSV: UV, face_id, u0, v0, u1, v1. (Java float values.)
 */
public final class H26MojangDefaultUvProbe {
    @SuppressWarnings({"unchecked", "rawtypes"})
    public static void main(String[] args) throws Exception {
        if (args.length != 10) {
            throw new IllegalArgumentException(
                "Expected bakerClass directionClass methodName UVClass and enumNames6");
        }
        Class<?> baker = Class.forName(args[0]);
        Class<?> direction = Class.forName(args[1]);
        String methodName = args[2];
        Class<?> uvClass = Class.forName(args[3]);
        Class<?> vectorInterface = Class.forName("org.joml.Vector3fc");
        Class<?> vectorClass = Class.forName("org.joml.Vector3f");
        Constructor<?> vectorConstructor =
            vectorClass.getConstructor(float.class, float.class, float.class);
        Method uv = baker.getDeclaredMethod(
            methodName, vectorInterface, vectorInterface, direction);
        uv.setAccessible(true);
        Method[] readers = new Method[4];
        for (int i = 0; i < 4; ++i) {
            readers[i] = uvClass.getDeclaredMethod("abcd".substring(i, i + 1));
            readers[i].setAccessible(true);
        }
        String[] dirs = {"down", "up", "north", "south", "west", "east"};
        Map<String, Object> enumerations = new HashMap<>();
        for (int i = 0; i < dirs.length; ++i) {
            enumerations.put(dirs[i], Enum.valueOf(
                (Class<? extends Enum>)direction.asSubclass(Enum.class), args[i + 4]));
        }
        BufferedReader input = new BufferedReader(
            new InputStreamReader(System.in, StandardCharsets.UTF_8));
        String line;
        int n = 0;
        while ((line = input.readLine()) != null) {
            if (line.isBlank()) continue;
            String[] fields = line.split("\t", -1);
            if (fields.length != 8) {
                throw new IllegalArgumentException("Expected 8 TSV fields");
            }
            String id = fields[0], face = fields[1];
            if (!id.matches("[a-zA-Z0-9_:.$/-]+") || !enumerations.containsKey(face)) {
                throw new IllegalArgumentException("Invalid original face key or direction");
            }
            float[] coordinates = new float[6];
            for (int i = 0; i < 6; ++i) {
                coordinates[i] = Float.parseFloat(fields[i + 2]);
                if (!Float.isFinite(coordinates[i])) {
                    throw new IllegalArgumentException("Non-finite source vertex");
                }
            }
            Object from = vectorConstructor.newInstance(
                coordinates[0], coordinates[1], coordinates[2]);
            Object to = vectorConstructor.newInstance(
                coordinates[3], coordinates[4], coordinates[5]);
            Object out = uv.invoke(null, from, to, enumerations.get(face));
            if (!uvClass.isInstance(out)) {
                throw new AssertionError("Original FaceBakery did not return original UV record");
            }
            StringBuilder result = new StringBuilder("UV\t").append(id);
            for (Method reader : readers) {
                float value = (float)reader.invoke(out);
                if (!Float.isFinite(value)) {
                    throw new AssertionError("Non-finite original vanilla UV");
                }
                result.append('\t').append(Float.toString(value));
            }
            System.out.println(result);
            ++n;
        }
        if (n == 0) {
            throw new AssertionError("No source model faces supplied");
        }
        System.err.println("H26_MOJANG_ORIGINAL_DEFAULT_FACE_UV_INVOKED=" + n);
    }
}
