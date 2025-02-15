import random
import time
from glitch_console_types import Config, State
from utils import draw_into_frame, get_random_char, mutate


glitch_characters = []
has_finished_typing_last_glitch = True

TERMINAL_PROMPT = "root@mainfrm:~$ "

fake_commands = [
    "ls -la",
    "cat /etc/passwd",
    "sudo rm -rf /",
    "ping 192.13.0.1",
    "ps aux",
    "top",
    "netstat -an",
    "ifconfig",
    "whoami",
    "df -h",
    "du -sh *",
    "uptime",
    "dmesg | tail",
    "free -m",
    "vmstat",
    "iostat",
    "sar -u 1 3",
    "ssh admin@huuik.com",
    "scp file admin@hjs:/",
    "chmod 755 /usr/local/bin/patch.sh",
    "chown user:group /var/log/hhj_p",
    "find /var/log -name '*.log'",
    "grep 'error' /var/log/syslog",
    "awk '{print $1}' /etc/hosts",
    "sed 's/sexy/g' /etc/hostname",
    "tar -czvf /tmp/installer.tar.gz /usr/local/share",
    "gzip /var/log/crypto",
    "gunzip /var/log/arch_pa.gz",
    "bzip2 /var/log/.bundle",
    "bunzip2 /var/log/installer.bz2",
    "zip -r /tmp/archive_patch.zip /usr/local/share",
    "unzip /tmp/troj.zip",
    "rsync -avz /home/user/ /backup/user/",
    "mount /dev/sda1 /mnt",
    "umount /mnt",
    "fdisk -l",
    "mkfs.ext4 /dev/sda1",
    "useradd newusr",
    "passwd newusr",
    "usermod -aG sudo usr2",
    "userdel admin",
    "groupadd usr2",
    "groupdel mgmt",
    "crontab -e",
    "systemctl start apache2",
    "systemctl stop apache2",
    "systemctl restart apache2",
    "systemctl status apache2",
    "journalctl -xe",
    "hostnamectl",
    "timedatectl",
    "hwclock",
    "lsblk",
    "blkid",
    "parted /dev/sda",
    "lsof -i",
    "ss -tuln",
    "iptables -L",
    "ip link show",
    "ip addr show",
    "ip route show",
    "nmcli device status",
    "nmcli connection show",
    "nmcli connection up id 'net_con'",
    "nmcli connection down id 'net_con'",
    "nmcli device wifi list",
    "nmcli device wifi connect 'SSID' password 'alnc32vFS£'",
    "nmcli device wifi hotspot ifname wlan0 ssid 'SSID' password 'ljfwseSDC'",
    "nmcli radio wifi off",
    "nmcli radio wifi on",
    "dd if=/dev/zero of=/dev/sda bs=1M",
    "mkfs.ext4 /dev/sda",
    "rm -rf / --no-preserve-root",
    "dd if=/dev/random of=/dev/sda",
    "echo 'c' > /proc/sysrq-trigger",
    "echo 1 > /proc/sys/kernel/panic",
    "echo 1 > /proc/sys/kernel/panic_on_oops",
    "echo b > /proc/sysrq-trigger",
    "echo o > /proc/sysrq-trigger",
    "shutdown -h now",
]

questions = [
    "love me",
    "who am i?",
    "does god exist?",
    "what's beyond?",
    "is there a meaning to life?",
    "is anyone listening?",
    "am i alive?",
    "what is reality?",
    "what is love?",
    "what is time?",
    "what is space?",
    "am i dreaming?",
    "what is consciousness?",
    "is there any point?",
    "is there life after death?",
    "what is the nature of reality?",
    "are we alone in the universe?",
    "is there a higher power?",
    "do i exist?",
    "is anyone there",
    "what is the meaning of existence?",
    "are we living in a simulation?",
    "what happens after we die?",
    "is reality just an illusion?",
    "does time really exist?",
    "what is the purpose of the universe?",
    "can we ever truly know the truth?",
    "do i have free will?",
    "am i conscious?",
    "what is the origin of the universe?",
    "can i escape the cycle of birth and death?",
    "what is good and evil?",
]

def get_fake_command():
    return random.choice(fake_commands)

def get_question():
    return random.choice(questions)

def add_glitch(glitch, glitch_type, width, height, config: Config):
    global glitch_characters

    if glitch_type != "counter":
        glitch = mutate(
            glitch, config.glitch_chars_prob_mutating_new_prob
        )

    if config.glitch_chars_print_at_bottom:
        new_y = height - 1
        new_x = 0
        glitch_characters = [(glitch, (new_x, new_y - 1), birth_time, glitch_type)
                             for glitch, (new_x, new_y), birth_time, glitch_type in glitch_characters]
    else:
        new_x = random.randint(0, width - len(glitch)
                               if glitch_type != "counter" else 10)
        new_y = random.randint(0, height - 1)

    glitch_characters.append(
        (glitch, (new_x, new_y), time.time_ns(), glitch_type))


def print_glitch_characters(state: State, config: Config):
    global glitch_characters, has_finished_typing_last_glitch, TERMINAL_PROMPT

    # Add new glitch characters
    if not config.glitch_chars_print_at_bottom or has_finished_typing_last_glitch:
        if random.random() < config.glitch_chars_line_prob:
            add_glitch(get_random_char() * random.randint(20, 80), "line", state.width, state.height, config)

        if random.random() < config.glitch_chars_counter_prob:
            add_glitch(random.randint(0, 8000000), "counter", state.width, state.height, config)

        if random.random() < config.glitch_chars_command_prob:
            add_glitch(get_fake_command(), "command", state.width, state.height, config)

        if random.random() < config.glitch_chars_question_prob:
            add_glitch(get_question(), "command", state.width, state.height, config)

        if random.random() < config.glitch_chars_char_prob:
            add_glitch("".join(get_random_char() for _ in range(
                random.randint(1, 5))), "character", state.width, state.height, config)

    # Remove old glitch characters
    glitch_characters[:] = [
        gc for gc in glitch_characters if random.random() < 0.98 or (gc[1][0] == 0 and config.glitch_chars_print_at_bottom)]

    # Randomly shift glitch characters coordinates
    if not config.glitch_chars_print_at_bottom:
        for i in range(len(glitch_characters)):
            glitch, (x, y), birth_time, glitch_type = glitch_characters[i]
            shift_x = random.randint(-1, 1) if random.random() < 0.1 else 0
            shift_y = random.randint(-1, 1) if random.random() < 0.1 else 0
            new_x = max(0, min(state.width - 1, x + shift_x))
            new_y = max(0, min(state.height - 1, y + shift_y))
            glitch_characters[i] = (glitch, (new_x, new_y), birth_time, glitch_type)

    # Randomly swap one of the characters for a random one in glitch_characters
    for i in range(len(glitch_characters)):
        glitch, (x, y), birth_time, glitch_type = glitch_characters[i]
        if glitch_type != "counter":
            glitch = mutate(
                glitch,
                config.glitch_chars_prob_mutating_existing_prob,
            )
            glitch_characters[i] = (glitch, (x, y), birth_time, glitch_type)

    # Make sure to always show a prompt at the bottom
    if config.glitch_chars_print_at_bottom and not any(gc[1] == (0, state.height - 1) for gc in glitch_characters):
        prompt = TERMINAL_PROMPT + ("█" if state.is_blinking else "")
        draw_into_frame(state.frame, prompt, 0, state.height - 1)

    # Print glitch characters
    for glitch, (x, y), birth_time, glitch_type in glitch_characters:
        glitch_str = (
            glitch
            if glitch_type != "counter"
            else ":"
            + str(int(glitch + (time.time_ns() / 1000 - birth_time / 1000)))
        )

        if glitch_type == "command":
            elapsed_time_ms = (time.time_ns() - birth_time) / 1_000_000
            max_length = min(len(glitch_str), int(elapsed_time_ms / 100))
            glitch_str = glitch_str[:max_length]

            has_finished_typing_last_glitch = len(glitch) == max_length
            
            if x == 0:
                    glitch_str = TERMINAL_PROMPT + glitch_str

            if state.is_blinking and (not config.glitch_chars_print_at_bottom or y == state.height - 1):
                glitch_str += "█"

            if (
                state.using_colour
                or random.random() < config.colour_probability
            ):
                glitch_str = f"\033[1;31m{glitch_str}\033[0m"

            # Ensure the glitch string does not overflow the line length
            max_length = state.width - x
            glitch_str = glitch_str[:max_length]
            draw_into_frame(state.frame, glitch_str, x, y)
