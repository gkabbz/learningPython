Setting Up Linux Machine

Install ubuntu extras
`sudo apt install ubuntu-restricted-extras`
Things like video in firefox won't work well without installing these

1. Mount storage drive
To mount the storage drive you need to:
- create a folder in the root to mount the drive to
    `mkdir /storage`
- Find the disk reference by running
    `sudo fdisk -l`
  You will get the disk reference such as `/dev/sdb2`
- Mount the disk 
  `sudo mount -t ntfs-3g -o user /dev/sdb2 /storage`
  Important to add the user parameter here because if you don't the disk will successfully mount but only the root will be able to access the contents. By adding the user option then users can see the files as well
- You can also do this by changing the `/etc/fstab` file by:
    - Editing the file `sudo vim /etc/fstab` and entering `/dev/sdb2  /storage    ext4    defaults,x-gvfs-show,user   0   0`
    Again here if you don't add the user option, you'll have the file access issue similar to above
    - Run `sudo mount /storage`    
2. Install Python3
3. Install Git
4. Install Google Cloud
4. Install Pycharm
5. Configure Pycharm - service accounts, environment variables
5. Install Airflow
6. Initialize Airflow
7. Install Synology Assistant
8. Install qBittorrent
9. Mount Synology Assistant
10. Add Google Drive
