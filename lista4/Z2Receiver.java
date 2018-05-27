import java.net.*;
import java.util.Hashtable;

public class Z2Receiver {
    private static final int datagramSize = 50;
    private int destinationPort;
    private DatagramSocket socket;

    private final static Object packetsLock = new Object();
    private volatile int nextIdx;
    private volatile Hashtable<Integer, Character> packets = new Hashtable<>();

    private ReceiverThread receiver;

    public Z2Receiver(int myPort, int destPort) throws Exception {
        destinationPort = destPort;
        socket = new DatagramSocket(myPort);
        receiver = new ReceiverThread();
        nextIdx = 0;
    }

    private boolean checkNext() {
        if (packets.containsKey(nextIdx)) {
            System.out.println("Received [" + nextIdx + "]: " + packets.get(nextIdx));
            ++nextIdx;
            return true;
        }
        return false;
    }

    public void checkReceived() {
        for (;;) {
            if (!checkNext()) break;
        }
    }

    class ReceiverThread extends Thread {
        public void run() {
            try {
                while (true) {
                    byte[] data = new byte[datagramSize];
                    DatagramPacket packet = new DatagramPacket(data, datagramSize);
                    socket.receive(packet);

                    Z2Packet p = new Z2Packet(packet.getData());
                    int idx = p.getIntAt(0);
                    char payload = (char) p.data[4];

                    synchronized (packetsLock) {
                        packets.put(idx, payload);
                    }

                    checkReceived();

                    packet.setPort(destinationPort);
                    socket.send(packet);
                }
            } catch (Exception e) {
                System.out.println("Z2Receiver.ReceiverThread.run: " + e);
            }
        }
    }

    public static void main(String[] args) throws Exception {
        Z2Receiver receiver = new Z2Receiver(
                Integer.parseInt(args[0]),
                Integer.parseInt(args[1])
        );
        receiver.receiver.start();
    }
}
