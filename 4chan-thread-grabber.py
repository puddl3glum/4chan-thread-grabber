#! /usr/bin/env python

import os
import shutil
import sys
import time

import requests

def get_images(save_location, board, thread_num):

  user_agent = {'User-agent': 'archive svc'}
  sess = requests.Session()
  sess.headers.update(user_agent)

  thread_url = f'http://a.4cdn.org/{board}/thread/{thread_num}.json'

  with sess.get(thread_url, ) as r:
    thread_json = r.text
    thread = r.json()

      # do req again

  images = [f"{p['tim']}{p['ext']}" for p in thread['posts'] if 'tim' in p]
  # print(images)
  # quit()

  
  for idx, image in enumerate(images):
    # print(post['tim'])

    # sleep a sec to follow da rulez
    time.sleep(1.1)

    image_url = f'http://i.4cdn.org/{board}/{image}'

    # download the images now:
    with sess.get(image_url) as i:
      # i.raw.decode_content = True
      # image_bin = i.raw
      image_bin = i.content
      # print(image_url)
      # print(i.text[:20])

    path = f'{save_location}/{thread_num}'

    if not os.path.exists(path):
      os.makedirs(path)

    with open(f'{path}/{thread_num}.json', 'w') as f:
      f.write(thread_json)

    with open(f'{path}/{image}', 'wb') as f:
      # r.raw.decode_content = True
      f.write(image_bin)
      # shutil.copyfileobj(image_bin, f)

    print(f'DONE {idx + 1} OUT OF {len(images)}')

def main(args):

  if len(args) < 3:
    msg = """
    ARGUMENTS:
      4chan-thread-image-grabber.py <save location> <board> <thread>

      save location: e.g. Y:4chan_stuff/midterm
      board: e.g. pol
      thread: e.g. 111111111
    """
    print(msg)
    quit()

  save_location = args[0]
  board = args[1]
  thread_num= args[2]

  get_images(save_location, board, thread_num)

if __name__ == '__main__':
  main(sys.argv[1:])