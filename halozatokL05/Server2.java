import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;
import java.net.*;
import java.io.*;
import java.util.ArrayList;
import java.util.HashMap;

public class Server2 {
    private static ServerSocket serverSocket;
    private static final HashMap<String, Socket> usersSockets = new HashMap<>();

    public static void main(String args[]) throws IOException, InterruptedException {
        serverSocket = new ServerSocket(6789);
        ArrayList<Thread> threads = new ArrayList<>();
        int height = 600, width = 800, n = 2;
        int[] h0 = { 0, 0, height/n, height/n };
        int[] w0 = { 0, width/n, 0, width/n };
        int[] h1 = { height/n, height/n, height, height };
        int[] w1 = { width/n, width, width/n, width };
        BufferedImage mandelbrot = new BufferedImage(width, height, BufferedImage.TYPE_INT_RGB);

        for (int i = 0; i < 4; i++) {
            ClientHandler2 clientHandler = new ClientHandler2(serverSocket.accept(), mandelbrot, h0[i], w0[i], h1[i], w1[i]);
            Thread thread = new Thread(clientHandler);
            threads.add(thread);

            System.out.println("Thread " + i + " added");
        }

        System.out.println("All threads added, starting them");
        for (Thread th : threads) {
            th.start();
        }
        for (Thread th : threads) {
            th.join();
        }

        System.out.println("All threads finished");
        File outputfile = new File("/home/baam0146/egyetem/halozatok/L05/src/image.jpg");
        ImageIO.write(mandelbrot, "jpg", outputfile);
    }

    protected void finalize() throws IOException {
        serverSocket.close();
    }
}
