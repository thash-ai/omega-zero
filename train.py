import argparse
import pathlib
import subprocess
import re
import datetime


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--test', action='store_true')
    parser.add_argument('--device-id', type=int, default=0)
    args = parser.parse_args()

    if args.test:
        n_thread = 1
        n_game = 10
        n_simulation = 1
        n_iter = 1
    else:
        n_thread = 50
        n_game = 2500
        n_simulation = 100
        n_iter = 10000

    start = datetime.datetime.now()

    model_dir_path = pathlib.Path('model')
    if model_dir_path.exists():
        print("model/ already exists")
    else:
        model_dir_path.mkdir()
        init_model_cmd = "python python/init_model.py"
        print(init_model_cmd)
        subprocess.check_call(init_model_cmd.split())

    mldata_dir_path = pathlib.Path('mldata')
    if mldata_dir_path.exists():
        generations = []
        for file_path in mldata_dir_path.glob('*.dat'):
            generations.append(int(file_path.name[:-4]))
        print(f"generations = {generations}")
        if len(generations) > 0:
            current = max(generations)
    else:
        mldata_dir_path.mkdir()
        current = 0

    print(f"\ncurrent generation = {current}")

    for generation in range(current, 100):
        mldata_path = mldata_dir_path / f'{generation}.dat'
        if mldata_path.exists():
            print(f"\n{mldata_path} already exists")
        else:
            self_play_cmd = f"./cpp/build/main {generation} {n_thread} {n_game} {n_simulation} {args.device_id}"
            print("\n" + self_play_cmd)
            subprocess.check_call(self_play_cmd.split())

            print("\nmerge mldata files")
            with open(f"mldata/{generation}.dat", 'wb') as output_file:
                for input_path in mldata_dir_path.glob(f"{generation}_*.dat"):
                    with open(input_path, 'rb') as input_file:
                        output_file.write(input_file.read())
                    input_path.unlink()

        model_path = model_dir_path / f"model_{generation+1}.pt"
        if model_path.exists():
            print(f"\n{model_path} already exists")
        else:
            model_train_cmd = f"python python/train_model.py {generation} --n-iter {n_iter} --device-id {args.device_id}"
            print("\n" + model_train_cmd)
            subprocess.check_call(model_train_cmd.split())

        end = datetime.datetime.now()
        print(f"\nelapsed time: {end - start}\n")