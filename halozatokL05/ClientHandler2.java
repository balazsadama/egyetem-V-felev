// https://medium.com/tech-and-the-city/multithreaded-server-23ad01aa2b98
// https://stackoverflow.com/questions/15889331/java-server-socket-sending-html-code-to-browser

import java.awt.image.BufferedImage;
import java.net.*;
import java.io.*;
import java.nio.file.Files;
import java.util.HashMap;
import java.util.Scanner;

public class ClientHandler2 implements Runnable {
    private Socket connectionSocket;
    private BufferedImage mandelbrot;
    private int h0, h1, w0, w1;

    public ClientHandler2(Socket connectionSocket, BufferedImage mandelbrot, int h0, int w0, int h1, int w1) {
        this.connectionSocket = connectionSocket;
        this.mandelbrot = mandelbrot;
        this.h0 = h0;
        this.h1 = h1;
        this.w0 = w0;
        this.w1 = w1;
    }

    @Override
    public void run() {
        DataInputStream clientOutput;
        DataOutputStream clientInput;
        String request = "";

        try {
            clientOutput = new DataInputStream(connectionSocket.getInputStream());
            clientInput = new DataOutputStream(connectionSocket.getOutputStream());

//            while (!request.equals("exit")) {
//                request = clientOutput.readLine();
//                System.out.println("Handler received: " + request);
//
//                clientInput.writeBytes("Roger that\n");
//            }

            clientInput.writeInt(h0);
            clientInput.writeInt(w0);
            clientInput.writeInt(h1);
            clientInput.writeInt(w1);

//            int rcpt = clientOutput.readInt();
//            System.out.println("handler received " + rcpt + " " + clientOutput.readInt());

            for (int y = h0; y < h1; y++) {
                for (int x = w0; x < w1; x++) {
                    mandelbrot.setRGB(x, y, clientOutput.readInt());
                }
            }

            connectionSocket.close();
        }
        catch (Exception e) {
            e.printStackTrace();
        }
    }


}
