import pygame
from glob import glob
import os
import json


assets = {}


def load_assets(folder):
  images = os.path.join(folder, "*.png")
  for image in glob(images):
    with open(image + ".meta") as file:
      meta = json.loads(file.read())
    name = os.path.split(image)[1].split(".")[0]
    image = pygame.image.load(image)
    if meta["convert"]:
      image.convert()
    assets[name] = image

def get_asset(name):
  return assets[name]
