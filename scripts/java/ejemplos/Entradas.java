package ejemplos;

import java.util.*;

/** Entradas literales; los valores por defecto corresponden al ejemplo del libro. */
public final class Entradas {
    public static int entero(String[] args, int i, int fallback) {
        return args.length > i ? Integer.parseInt(args[i].trim()) : fallback;
    }
    public static boolean logico(String[] args, int i, boolean fallback) {
        if (args.length <= i) return fallback;
        if (!args[i].equals("true") && !args[i].equals("false"))
            throw new IllegalArgumentException("Usa true o false.");
        return Boolean.parseBoolean(args[i]);
    }
    public static int[] arreglo(String[] args, int i, int[] fallback) {
        if (args.length <= i) return fallback;
        String s = args[i].trim();
        if (!s.startsWith("{") || !s.endsWith("}")) throw new IllegalArgumentException("Usa un arreglo entre llaves.");
        s = s.substring(1, s.length()-1).trim();
        if (s.isEmpty()) return new int[0];
        String[] pieces = s.split(",", -1);
        int[] arr = new int[pieces.length];
        for (int j=0; j<arr.length; j++) arr[j] = Integer.parseInt(pieces[j].trim());
        return arr;
    }
    public static int[][] matriz(String[] args, int i, int[][] fallback) {
        if (args.length <= i) return fallback;
        String s = args[i].trim();
        if (!s.startsWith("{") || !s.endsWith("}")) throw new IllegalArgumentException("Usa una matriz entre llaves.");
        s = s.substring(1, s.length()-1).trim();
        if (s.isEmpty()) return new int[0][];
        List<int[]> rows = new ArrayList<>();
        int position=0;
        while(position<s.length()) {
            int end=s.indexOf('}', position);
            if (end<0 || s.charAt(position)!='{') throw new IllegalArgumentException("Formato de matriz inválido.");
            rows.add(arreglo(new String[]{s.substring(position,end+1)},0,null));
            position=end+1;
            while(position<s.length() && Character.isWhitespace(s.charAt(position))) position++;
            if (position<s.length()) {
                if(s.charAt(position++)!=',') throw new IllegalArgumentException("Separa las filas con comas.");
                while(position<s.length() && Character.isWhitespace(s.charAt(position))) position++;
                if(position==s.length()) throw new IllegalArgumentException("Falta una fila.");
            }
        }
        return rows.toArray(new int[0][]);
    }
}
