import pwd
import grp

def uid_to_name(uid):
    return pwd.getpwuid( uid ).pw_name


def gid_to_name(gid):
    return grp.getgrgid( gid ).gr_name


def name_to_uid(name):
    return pwd.getpwnam( name ).pw_uid


def name_to_gid(name):
    return grp.getgrnam( name ).gr_gid


