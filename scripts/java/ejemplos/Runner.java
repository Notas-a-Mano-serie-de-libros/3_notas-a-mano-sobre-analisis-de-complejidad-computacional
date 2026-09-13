package ejemplos;

import java.io.*;
import java.lang.reflect.*;

/** Invoca el main publicado y captura la salida para Pages. */
public final class Runner {
    public static String execute(String className, String encoded) {
        ByteArrayOutputStream bytes = new ByteArrayOutputStream();
        PrintStream original = System.out;
        PrintStream output = new PrintStream(new OutputStream() {
            int count;
            public void write(int value) throws IOException {
                if (++count > 50000) throw new IOException("La salida superó 50 000 caracteres.");
                bytes.write(value);
            }
        });
        boolean failed = false;
        try {
            System.setOut(output);
            String[] args = encoded.isEmpty() ? new String[0] : encoded.split("\n", -1);
            Class.forName(className).getMethod("main", String[].class).invoke(null, (Object) args);
            if (output.checkError()) throw new IllegalStateException("La salida superó 50 000 caracteres.");
        } catch (Throwable error) {
            failed = true;
            if (error instanceof InvocationTargetException) error = error.getCause();
            output.println(error.getClass().getSimpleName() + ": " + error.getMessage());
            if(output.checkError()) return "ERROR\n" + new String(bytes.toByteArray()) + "\nLa salida superó 50 000 caracteres.";
        } finally {
            System.setOut(original);
            output.close();
        }
        return (failed ? "ERROR\n" : "OK\n") + new String(bytes.toByteArray());
    }
    public static void main(String[] args) { System.out.print(execute(args[0], args.length>1 ? args[1] : "")); }
}
