import airsim
import numpy as np
import cv2
import os

# >------>>>  AirSim settings   <<<------< #
client = airsim.MultirotorClient()      # Connect to AirSim
client.confirmConnection()             # Verify connection and print status: Connected! Client Ver:1 (Min Req: 1), Server Ver:1 (Min Req: 1)

i = 0
while True:
    # Get segmentation image in various formats
    responses = client.simGetImages([
        airsim.ImageRequest("3", airsim.ImageType.Scene, False, False),          # Scene vision image in uncompressed RGBA array
        airsim.ImageRequest("3", airsim.ImageType.Segmentation, False, False)])  # Segmentation image in uncompressed RGBA array
    print('Retrieved images: %d', len(responses))

    # Save segmentation images in different formats
    for idx, response in enumerate(responses):
        filename = 'IMG/seg_' + str(i) + '_' + str(idx)

        if response.pixels_as_float:
            print("Type %d, size %d" % (response.image_type, len(response.image_data_float)))
            # airsim.write_pfm(os.path.normpath(filename + '.pfm'), airsim.get_pfm_array(response))

        elif response.compress:  # PNG format
            print("Type %d, size %d" % (response.image_type, len(response.image_data_uint8)))
            # airsim.write_file(os.path.normpath(filename + '.png'), response.image_data_uint8)

        else:  # Uncompressed array - numpy demo
            print("Type %d, size %d" % (response.image_type, len(response.image_data_uint8)))
            img1d = np.fromstring(
                response.image_data_uint8, dtype=np.uint8)  # Get numpy array
            img_rgb = img1d.reshape(
                response.height, response.width, 3)  # Reshape to 3-channel image array H X W X 3
            cv2.imwrite(os.path.normpath(filename + '.png'), img_rgb)  # Save as PNG


    i += 1

