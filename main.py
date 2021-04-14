import os.path
import shutil
import glob
import logging
import cv2
import insightface
import numpy as np
from mxnet import MXNetError

logger = logging.getLogger()
age_ranges = [1, 8, 13, 18, 30, 50, 120]
age_groups = {
    'childhood': range(0, 8),
    'puberty': range(8, 13),
    'adolescence': range(13, 18),
    'adulthood': range(18, 30),
    'middle_age': range(30, 50),
    'seniority': range(50, 120),
}

def build_image_age_dict(path, delimiter="|"):
    paths = glob.glob(path + '/**/*.*', recursive=True)
    age_dict = {}
    for filepath in paths:
        # find age label for WIKIAge
        filename, ext = os.path.splitext(os.path.basename(filepath))
        try:
            lbl_age = float(filename.split(delimiter)[-1])
        except Exception as e:
            logger.warn(e)
            continue
        for lbl, irange in age_groups.items():
            if min(irange) <= lbl_age <= max(irange):
                break
        age_dict[filepath] = lbl_age

    return age_dict

def detect_age(img: np.ndarray, model, ctx_id=-1):
    """
    # Use CPU to do all the job. Please change ctx-id to a positive number if you have GPUs
    """
    model.prepare(ctx_id=ctx_id, nms=0.4)
    faces = model.get(img)

    return [face.age for face in faces]

def load_image_to_array(filepath):
    data = cv2.imread(filepath)
    return data

if __name__ == '__main__':

    import ImageLabelingPackage as lp
    import argparse, sys

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_dir", required=True)
    parser.add_argument("-o", "--output_dir", required=True)
    parser.add_argument("-e", "--err_dir", required=True)
    parser.add_argument("-u", "--unk_dir", required=True)
    parser.add_argument("-a", "--age", help="threshold", default=16)
    args = parser.parse_args()
    # ageDetector = lp.ArcFaceAgeLabeler()



    paths = glob.glob(args.input_dir + '/**/*.*', recursive=True)
    paths = [path for path in paths if path.split(".")[-1].lower() in ["jpeg", "jpg", "png", "tif", "tiff", "webp"]]
    age_dict = build_image_age_dict(args.input_dir, delimiter="|")

    for img_path in paths:
        if "reference_img" in img_path:
            continue
        model = insightface.app.FaceAnalysis()
        basename = os.path.basename(img_path)
        try:
            img = load_image_to_array(img_path)

            print(img_path)
            pred_ages = detect_age(img, model=model)
            pred_age = min(pred_ages) if len(pred_ages) > 0 else 999999
            true_age = age_dict[img_path]
            print(f"image {basename} has true age = {true_age} and predict age = {pred_age}")

            if pred_age - true_age < args.age or pred_age < 26:# the second condition is because the estimator not good with less than 10 years old, so make it less strict
                shutil.move(img_path, os.path.join(args.output_dir, basename))
            else:
                shutil.move(img_path, os.path.join(args.err_dir, basename))
        except MXNetError as e:
            shutil.move(img_path, os.path.join(args.unk_dir, basename))
            logger.warning(e)
        except KeyError as e:
            shutil.move(img_path, os.path.join(args.unk_dir, basename))
            logger.warning(e)


