from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

class VolumeController:
    def __init__(self):
        self.volume = self._get_volume_interface()
        self.current_volume = self.get_current_volume()

    def _get_volume_interface(self):
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        return cast(interface, POINTER(IAudioEndpointVolume))

    def get_current_volume(self):
        # Returns current volume as a percentage (0-100)
        vol = self.volume.GetMasterVolumeLevelScalar()
        return int(vol * 100)

    def increase_volume(self, increment=2):
        self.current_volume = self.get_current_volume()
        new_volume = min(self.current_volume + increment, 100)
        self.set_system_volume(new_volume)
        self.current_volume = new_volume

    def decrease_volume(self, decrement=2):
        self.current_volume = self.get_current_volume()
        new_volume = max(self.current_volume - decrement, 0)
        self.set_system_volume(new_volume)
        self.current_volume = new_volume

    def set_system_volume(self, volume):
        # Set system volume (0-100)
        volume = max(0, min(volume, 100))
        self.volume.SetMasterVolumeLevelScalar(volume / 100, None)

    def mute_volume(self):
        self.volume.SetMute(1, None)

    def unmute_volume(self):
        self.volume.SetMute(0, None)

    def is_muted(self):
        return self.volume.GetMute() == 1