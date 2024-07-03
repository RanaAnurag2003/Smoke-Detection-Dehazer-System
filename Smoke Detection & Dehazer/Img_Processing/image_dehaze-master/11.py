from aiortc import RTCIceServer, RTCPeerConnection, RTCSessionDescription
from aiortc.contrib.media import MediaBlackhole, MediaStreamTrack
from PIL import ImageGrab
import asyncio

class ScreenCaptureTrack(MediaStreamTrack):
    def __init__(self):
        self.screenshare = None

    async def recv(self):
        img = ImageGrab.grab()  # Capture the screen using Pillow
        frame = img.tobytes()
        pts, time_base = await self.next_timestamp()
        return RTCVideoFrame(width=img.width, height=img.height, data=frame, timestamp=pts, time_base=time_base)

async def run(pc):
    pc_id = "streamer"
    servers = None
    pc = RTCPeerConnection()
    pc_id = "streamer"

    @pc.on("datachannel")
    def on_datachannel(channel):
        @channel.on("message")
        def on_message(message):
            print("Received message:", message)

    @pc.on("iceconnectionstatechange")
    def on_iceconnectionstatechange():
        print("ICE connection state:", pc.iceConnectionState)
        if pc.iceConnectionState == "failed":
            print("ICE connection failed, restarting")
            pc.restartIce()

    pc.createDataChannel("chat")

    # Add a screen capture track
    capture_track = ScreenCaptureTrack()
    pc.addTrack(capture_track)

    await pc.setLocalDescription(await pc.createOffer())
    # You'll need to replace 'ws://your_server_address_here' with your actual WebRTC server address.
    pc.remoteDescription = RTCSessionDescription(sdp="", type="offer")
    pc.addIceCandidate(RTCIceCandidate(candidate="candidate", sdpMLineIndex=0))

if __name__ == "__main__":
    pc = RTCPeerConnection()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(pc))
