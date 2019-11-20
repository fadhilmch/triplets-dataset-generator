#!/usr/bin/python

import os
import re
import json
import pandas as pd
import itertools
import random
from argparse import ArgumentParser

ext = 'jpg|jpeg|bmp|png|ppm|JPG|JPEG'


def get_files_list(directory_path, class_name=None):
    if class_name:
        return [file for root, _, files_list in os.walk(os.path.join(directory_path, class_name)) for file in files_list if re.match(r'([\w]+\.(?:' + ext + '))', file)]
    else:
        return [file for root, _, files_list in os.walk(directory_path) for file in files_list if re.match(r'([\w]+\.(?:' + ext + '))', file)]


def main(args):
    if args.dataset_dir == None:
        raise ValueError(
            'Path to dataset directory is required!')
    if args.pair_dir == None:
        raise ValueError(
            'Path to pair file directory is required!')
    print('Running program to sample triplet pair from Street2Shop Dataset...')
    images_path = args.dataset_dir
    classes_list = [dir_ for dir_ in os.listdir(
        images_path) if os.path.isdir(os.path.join(images_path, dir_))]

    # Handle error
    if len(classes_list) == 0:
        raise ValueError(
            'Your images directory does not contain class directories')
    if args.n_neg_class > len(classes_list)-1:
        raise ValueError(
            'The number of negative classes sample you want is exceeding the number of classes you have. Use smaller number of negative class samples')

    # Overwriting the existing file
    if args.overwrite:
        print('Overwrite the existing file....')
        triplet_file = open(args.output_file, 'w+')
        triplet_file.close()

    triplet_file = open(args.output_file, '+a')
    count_pairs = {class_name: 0 for class_name in classes_list}

    for index, class_name in enumerate(classes_list):
        print('\n=======> Sampling triplet for class: ' + class_name)
        pair_file = 'json/train_pairs_' + class_name + '.json'
        try:
            file_meta = open(args.pair_dir + pair_file, 'r')
        except ValueError:
            print("You don't have the pair file(s)")
        pair_data = json.load(file_meta)
        file_meta.close()
        neg_classes = random.sample([x for x in range(
            0, index)]+[x for x in range(index+1, len(classes_list))], k=args.n_neg_class)
        neg_file_paths = [os.path.join(images_path, classes_list[neg_class])
                          for neg_class in neg_classes]
        n_neg_images = [len(get_files_list(x)) for x in neg_file_paths]

        print('Total images: ' + str(len(pair_data)) + ' images')
        existing_images = set(get_files_list(images_path, class_name))
        for data in pair_data:
            if (str(data['photo'])+'.JPEG') not in existing_images:
                pair_data.remove(data)
        print('Total available images: ' +
              str(len(pair_data)) + ' images')
        pair_df = pd.DataFrame.from_dict(pair_data)
        product_list = pair_df['product'].unique()
        for product in product_list:
            pos_images = pair_df[pair_df['product']
                                 == product]['photo'].tolist()
            com_images = list(itertools.combinations(pos_images, 2))
            for com in com_images:
                neg_index_list = [[random.randint(
                    0, n_neg_image-1) for n in range(args.n_neg)] for n_neg_image in n_neg_images]
                # neg_index = random.randint(0, n_neg_images[0]-1)
                for idx, class_index in enumerate(neg_index_list):
                    for neg_index in class_index:
                        triplet_list = [images_path + class_name + '/' + str(img) + '.JPEG' for img in com] + [
                            neg_file_paths[idx] + '/' + get_files_list(neg_file_paths[idx])[neg_index]]
                        triplet_file.write(','.join(triplet_list)+'\n')
                        # triplet_list = [images_path + class_name + '/' + str(img) + '.JPEG' for img in com] + [
                        #     neg_file_paths[0] + '/' + get_files_list(neg_file_paths[0])[neg_index]]
                        # triplet_file.write(','.join(triplet_list) + '\n')
                        count_pairs[class_name] += 1
        print('Total triplet pairs: ' + str(count_pairs[class_name]))
    print('\nTotal new triplet pairs added: ' + str(sum(count_pairs.values())))
    triplet_file.close()


if __name__ == '__main__':
    parser = ArgumentParser()

    # Data handling parameters
    parser.add_argument('--dataset_dir', dest='dataset_dir',
                        type=str)
    parser.add_argument('--pair_dir', dest='pair_dir',
                        type=str)
    parser.add_argument('--output_file', dest='output_file',
                        type=str, default='triplet_pairs.txt')
    parser.add_argument('--number_neg_class',
                        dest='n_neg_class', type=int, default=1)  # Number of negative classes for negative sampling
    parser.add_argument('--number_neg_sample',
                        dest='n_neg', type=int, default=1)  # Number of negative samples for each negative class
    parser.add_argument('--overwrite', dest='overwrite',
                        action='store_true')
    parser.add_argument('--crop', dest='crop',
                        action='store_true')
    args = parser.parse_args()

    main(args)
    print('Output file: ' + args.output_file)
    print('Finished')

    exit(0)
