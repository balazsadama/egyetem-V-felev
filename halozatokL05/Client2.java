import java.io.*;
import java.net.Socket;
import java.util.Scanner;

public class Client2 {
    public static void main(String args[]) throws Exception{

        Socket clientSocket;
        DataOutputStream clientOutputStream;
        DataInputStream inputFromServer;
//        BufferedReader serverReader;
        Scanner sc = new Scanner(System.in);

        clientSocket = new Socket("localhost", 6789);
        clientOutputStream = new DataOutputStream(clientSocket.getOutputStream());
//        serverReader = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
        inputFromServer = new DataInputStream(clientSocket.getInputStream());

//        String inp = "";
//        String serverOutput;
//        while (!inp.equals("exit")) {
//            inp = sc.nextLine();
//            clientOutputStream.writeBytes(inp + "\n");
//
//            serverOutput = serverReader.readLine();
//            System.out.println(serverOutput);
//        }

        int h0, h1, w0, w1;
        double zx, zy, cX, cY, tmp;
        final int MAX_ITER = 570;
        final double ZOOM = 150;

        h0 = inputFromServer.readInt();
        w0 = inputFromServer.readInt();
        h1 = inputFromServer.readInt();
        w1 = inputFromServer.readInt();

//        Thread.sleep(5000);
        System.out.println("got these: " + h0 + " " + w0 + " " + h1 + " " + w1);

//        clientOutputStream.writeInt(69);
//        clientOutputStream.writeInt(420);

        for (int y = h0; y < h1; y++) {
            for (int x = w0; x < w1; x++) {
                zx = zy = 0;
                cX = (x - 400) / ZOOM;
                cY = (y - 300) / ZOOM;
                int iter = MAX_ITER;
                while (zx * zx + zy * zy < 4 && iter > 0) {
                    tmp = zx * zx - zy * zy + cX;
                    zy = 2.0 * zx * zy + cY;
                    zx = tmp;
                    iter--;
                }
//                I.setRGB(x, y, iter | (iter << 8));
                clientOutputStream.writeInt(iter | (iter << 8));
            }
        }

        clientSocket.close();
    }
}
