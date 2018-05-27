import java.net.*;
import java.util.*;

public class Z2Forwarder {
    private static final int datagramSize = 50;

    // PARAMETRY W MILISEKUNDACH
    private static final int capacity = 1000;
    private static final int minDelay = 2000;
    private static final int maxDelay = 10000;
    private static final int sleepTime = 100;

    // NIEZAWODNOSC PRZEKAZYWANIA PAKIETU
    private static final double reliability = 0.80;
    // PRAWDOPODOBIENSTWO ZDUPLIKOWANIA PAKIETU
    private static final double duplicatePpb = 0.1;

    private int destinationPort;

    private DatagramSocket socket;
    private DatagramPacket[] buffer;
    private final Object bufferLock = new Object();
    private int[] delay;

    private Receiver receiver;
    private Sender sender;
    private Random random;

    public Z2Forwarder(int myPort, int destPort) throws Exception {
        destinationPort = destPort;
        socket = new DatagramSocket(myPort);
        buffer = new DatagramPacket[capacity];
        delay = new int[capacity];
        random = new Random();
        receiver = new Receiver();
        sender = new Sender();
    }

    class Receiver extends Thread {
        void addToBuffer(DatagramPacket packet) {
            if (random.nextDouble() > reliability) return;

            synchronized (bufferLock) {
                int i = 0;
                while (i < capacity && buffer[i] != null) {
                    i++;
                }

                if (i < capacity) {
                    delay[i] = minDelay + (int)(random.nextDouble() * (maxDelay - minDelay));
                    buffer[i] = packet;
                }
            }
        }

        public void run() {
            while (true) {
                DatagramPacket packet = new DatagramPacket(new byte[datagramSize], datagramSize);
                try {
                    socket.receive(packet);
                    addToBuffer(packet);
                    while (random.nextDouble() < duplicatePpb) {
                        addToBuffer(packet);
                    }

                } catch (java.io.IOException e) {
                    System.out.println("Forwader.Receiver.run: " + e);
                }
            }
        }
    }

    class Sender extends Thread {
        void checkBuffer() throws java.io.IOException {
            synchronized (bufferLock) {
                int i;
                for (i = 0; i < capacity; i++)
                    if (buffer[i] != null) {
                        delay[i] -= sleepTime;
                        if (delay[i] <= 0) {
                            buffer[i].setPort(destinationPort);
                            socket.send(buffer[i]);
                            buffer[i] = null;
                        }
                    }
            }
        }


        public void run() {
            try {
                while (true) {
                    checkBuffer();
                    sleep(sleepTime);
                }
            } catch (Exception e) {
                System.out.println("Forwader.Sender.run: " + e);
            }
        }

    }

    public static void main(String[] args) throws Exception {
        Z2Forwarder forwarder = new Z2Forwarder(
                Integer.parseInt(args[0]),
                Integer.parseInt(args[1])
        );
        forwarder.sender.start();
        forwarder.receiver.start();
    }
}
