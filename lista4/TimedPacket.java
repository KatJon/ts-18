class TimedPacket{
    private int retransmitTime;
    private Z2Packet packet;
    
    public TimedPacket(int retransmitTime, Z2Packet packet) {
        this.retransmitTime = retransmitTime;
        this.packet = packet;
    }

    public boolean shouldRetransmit(int currentTime) {
        return currentTime >= retransmitTime;
    }

    public Z2Packet getPacket() {
        return packet;
    }

}