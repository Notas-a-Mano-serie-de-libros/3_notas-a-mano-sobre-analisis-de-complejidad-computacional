import java.util.*;
import java.math.*;
import java.lang.reflect.*;

class BookReviewChecks {
    static int searchCases = 0, sortCases = 0, scalarCases = 0;
    static void require(boolean value) {
        if (!value) throw new AssertionError("Resultado diferente de la referencia");
    }
    static Object call(int id, String name, Class<?>[] types, Object... args) throws Exception {
        Class<?> cls = Class.forName("L" + id);
        return cls.getDeclaredMethod(name, types).invoke(cls.getDeclaredConstructor().newInstance(), args);
    }
    static void searches(int[] arr) throws Exception {
        int[] sorted = arr.clone(); Arrays.sort(sorted);
        for (int x = -1; x <= 4; x++) {
            boolean expected = Arrays.binarySearch(sorted, x) >= 0;
            for (int id : new int[]{57,58,59,61,62,63,64}) {
                
                boolean actual;
                if (id == 57 || id == 61 || id == 62)
                    actual = (boolean) call(id, "buscar", new Class[]{int[].class,int.class}, sorted,x);
                else actual = (boolean) call(id, "buscar", new Class[]{int[].class,int.class,int.class,int.class}, sorted,0,sorted.length-1,x);
                require(actual == expected); searchCases++;
            }
        }
    }
    static void sorts(int[] arr) throws Exception {
        int[] expected = arr.clone(); Arrays.sort(expected);
        for (int id : new int[]{48,65,66,67,68,69,70,71,72}) {
            
            int[] actual = arr.clone();
            if (id == 48 || id == 70 || id == 71)
                call(id,"ordenar",new Class[]{int[].class,int.class,int.class},actual,0,actual.length-1);
            else call(id,"ordenar",new Class[]{int[].class},(Object)actual);
            require(Arrays.equals(actual,expected)); sortCases++;
        }
    }
    static String failure(int id, String name, Class<?>[] types, Object... args) throws Exception {
        try { call(id,name,types,args); return "sin excepción"; }
        catch (InvocationTargetException e) { return e.getCause().getClass().getSimpleName(); }
    }
    public static void main(String[] args) throws Exception {
        Random random = new Random(20260912);
        searches(new int[0]); sorts(new int[0]);
        for (int n = 1; n <= 30; n++) {
            for (int trial = 0; trial < 100; trial++) {
                int[] arr = new int[n];
                for (int i = 0; i < n; i++) arr[i] = random.nextInt(4);
                searches(arr); sorts(arr);
            }
        }
        for (int n = 1; n <= 30; n++) {
            int[] arr = new int[n];
            for (int i = 0; i < n; i++) arr[i] = i * 3;
            for (int x = -1; x <= n * 3; x++) {
                // Excluye el caso singleton encontrado que provoca den=0 en el original.
                
                try {
                    boolean actual = (boolean) call(60,"buscar",new Class[]{int[].class,int.class,int.class,int.class},arr,0,n-1,x);
                    require(actual == (Arrays.binarySearch(arr,x) >= 0)); searchCases++;
                } catch (InvocationTargetException e) {
                    throw e;
                }
            }
        }
        int[] fib = {0,1,1,2,3,5,8,13,21,34,55};
        for (int n = 0; n < fib.length; n++) {
            require(L45.fibonacci(n) == fib[n]); require(L46.fibonacci(n) == fib[n]);
            require(new L21().fibonacciBigInteger(n).intValue() == fib[n]); scalarCases += 3;
        }
        int fact = 1;
        for (int n = 0; n <= 12; n++) {
            if (n > 0) fact *= n;
            require(L44.factorial(n) == fact); require(L42.f(n) == fact); scalarCases += 2;
        }
        for (int a = -3; a <= 3; a++) for (int n = -10; n <= 10; n++) {
            if (a == 0 && n < 0) continue;
            double expected = Math.pow(a,n), actual = L47.potencia(a,n);
            require(Math.abs(actual-expected) <= Math.max(1,Math.abs(expected))*1e-12); scalarCases++;
        }
        for (int n = 0; n <= 1000; n++) {
            boolean prime = BigInteger.valueOf(n).isProbablePrime(30);
            require(new L33().esPrimo(n) == prime); require(new L39().esPrimoAnidado(n) == prime); scalarCases += 2;
        }
        require(Arrays.deepEquals(L16.inicializarMatriz(2,3),new int[][]{{1,1,1},{1,1,1}})); scalarCases++;
        require(new L36().multiplicar(new int[][]{{1,2},{3,4}},new int[][]{{2,0},{1,2}})[1][1] == 8); scalarCases++;
        require(new L51().mcd(48,18)==6); require(new L52().combinar(5,2)==10);
        require(new L53().sumaArreglo(new int[]{1,2,3},3)==6);
        require(new L55().invertir("abc").equals("cba")); require(new L56().sumaDigitos(123)==6); scalarCases+=5;
        String interpolation = failure(60,"buscar",new Class[]{int[].class,int.class,int.class,int.class},new int[]{7},0,0,7);
        String jump = failure(61,"buscar",new Class[]{int[].class,int.class},new int[0],7);
        String exponential = failure(62,"buscar",new Class[]{int[].class,int.class},new int[0],7);
        String radix = failure(72,"ordenar",new Class[]{int[].class},(Object)new int[0]);
        String radixNegative = failure(72,"ordenar",new Class[]{int[].class},(Object)new int[]{-1,2});
        require(interpolation.equals("sin excepción")); require(jump.equals("sin excepción"));
        require(exponential.equals("sin excepción")); require(radix.equals("sin excepción"));
        require(radixNegative.equals("sin excepción"));
        require((boolean) call(60,"buscar",new Class[]{int[].class,int.class,int.class,int.class},new int[]{7},0,0,7));
        require(!(boolean) call(61,"buscar",new Class[]{int[].class,int.class},new int[0],7));
        require(!(boolean) call(62,"buscar",new Class[]{int[].class,int.class},new int[0],7));
        require(L47.potencia(2,Integer.MIN_VALUE)==0.0);
        require(L47.potencia(2,-1024)>0.0);
        require(failure(44,"factorial",new Class[]{int.class},13).equals("ArithmeticException"));
        require(failure(46,"fibonacci",new Class[]{int.class},47).equals("ArithmeticException"));
        require(new L33().esPrimo(Integer.MAX_VALUE));
        require(new L51().mcd(-48,-18)==6);
        require(new L55().invertir("A\uD83D\uDE00B").equals("B\uD83D\uDE00A"));
        sorts(new int[]{Integer.MIN_VALUE,Integer.MAX_VALUE,-1,0,1});
        for (int trial=0;trial<100;trial++) {
            int[] arr = new int[20];
            for (int i=0;i<arr.length;i++) arr[i]=random.nextInt();
            sorts(arr);
        }
        java.io.ByteArrayOutputStream moves = new java.io.ByteArrayOutputStream();
        java.io.PrintStream stdout = System.out;
        System.setOut(new java.io.PrintStream(moves));
        new L54().hanoi(3,'A','C');
        System.setOut(stdout);
        String[] lines = moves.toString().trim().split("\\R");
        require(lines.length==7);
        Map<Character,Deque<Integer>> towers = new HashMap<>();
        for (char name : new char[]{'A','B','C'}) towers.put(name,new ArrayDeque<>());
        for (int disk=3;disk>=1;disk--) towers.get('A').push(disk);
        for (String line:lines) {
            Deque<Integer> from=towers.get(line.charAt(0)), to=towers.get(line.charAt(5));
            int disk=from.pop(); require(to.isEmpty() || to.peek()>disk); to.push(disk);
        }
        require(towers.get('C').size()==3);
        System.out.printf(Locale.ROOT,
            "{\"search_success_cases\":%d,\"sort_success_cases\":%d,\"scalar_success_cases\":%d,"+
            "\"regressions\":{\"interpolation_singleton\":\"%s\",\"jump_empty\":\"%s\",\"exponential_empty\":\"%s\","+
            "\"radix_empty\":\"%s\",\"radix_negative\":\"%s\",\"power_min_exponent\":\"0.0 correcto\","+
            "\"factorial_13_overflow_detected\":true,\"fibonacci_47_overflow_detected\":true}}%n",
            searchCases,sortCases,scalarCases,interpolation,jump,exponential,radix,radixNegative);
    }
}
