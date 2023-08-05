class Blorgle:
    def __init__(self, z):
        self.z_scope = z

    def get_z_scope(self):
        return self.z_scope


def calibrate_blorgle(blorgle_manifest_counts):
    calibration_sum = 0
    calibration_hash = ""
    for manifest_count in blorgle_manifest_counts:
        calibration_sum += manifest_count
        calibration_hash += str(manifest_count)
    return calibration_sum, calibration_hash
