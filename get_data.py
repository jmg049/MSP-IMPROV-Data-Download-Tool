import getpass
import asyncio
import shutil
import os
from pathlib import Path

username = "MSP-IMPROV"
DEBUG = True


def move_all_up_one_level(dir):
    print(dir)
    print(os.listdir(dir))
    for x in [
        os.path.join(dir, d)
        for d in os.listdir(dir)
        if os.path.isdir(os.path.join(dir, d))
    ]:
        ## move the directories up one level
        if DEBUG:
            print(f"Moving {x} to {Path(dir).parent}")
        shutil.move(x, Path(dir).parent)

    os.rmdir(dir)
    if DEBUG:
        print(f"Removed {dir}")
    return


async def run_command(command):
    process = await asyncio.create_subprocess_shell(command)
    await process.wait()


async def download_commands(commands):
    await asyncio.gather(*(run_command(command) for command in commands))


if __name__ == "__main__":

    password = getpass.getpass("Enter your password: ")

    wget_args = {
        "--user": username,
        "--password": password,
    }

    user_pass_str = f'--user {username} --password "{password}"'

    # Directory where you want to save the files

    # Download the data
    commands = [
        f"wget --recursive --directory-prefix=./MSP_IMPROV {user_pass_str} http://www.lab-msp.com/MSP-IMPROV/Audio/",
        f"wget --recursive --directory-prefix=./MSP_IMPROV {user_pass_str} http://www.lab-msp.com/MSP-IMPROV/Video/ ",
        f"wget --directory-prefix=./MSP_IMPROV {user_pass_str} http://www.lab-msp.com/MSP-IMPROV/Evaluation.txt",
        f"wget --directory-prefix./MSP_IMPROV {user_pass_str} http://www.lab-msp.com/MSP-IMPROV/Human_Transcriptions.zip",
        f"wget --directory-prefix=./MSP_IMPROV {user_pass_str} http://www.lab-msp.com/MSP-IMPROV/Phonetic_Alignments.zip",
        f"wget --directory-prefix=./MSP_IMPROV {user_pass_str} http://www.lab-msp.com/MSP-IMPROV/Readme.txt",
    ]

    asyncio.run(download_commands(commands))

    for root, dirs, files in os.walk("./MSP_IMPROV"):
        for file in files:
            if "index.html" in file:
                if DEBUG:
                    print(f"Removing {os.path.join(root, file)}")
                os.remove(os.path.join(root, file))

    move_all_up_one_level("./MSP_IMPROV/www.lab-msp.com")
    move_all_up_one_level("./MSP_IMPROV/MSP-IMPROV")

    if os.path.exists("./MSP_IMPROV/spicons"):
        shutil.rmtree("./MSP_IMPROV/spicons")
