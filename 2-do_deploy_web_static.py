from fabric.api import *
import os.path


env.hosts = ['<IP web-01>', '<IP web-02>']
env.user = '<your_username>'
env.key_filename = '/path/to/your/private_key'


def do_deploy(archive_path):
        if not os.path.exists(archive_path):
                    return False
                    
                    # Upload the archive to /tmp/ directory on the web servers
                        put(archive_path, '/tmp/')
                            
                                # Extract the archive to /data/web_static/releases/<archive filename without extension> on the web servers
                                    archive_filename = os.path.basename(archive_path)
                                        release_path = '/data/web_static/releases/{}'.format(os.path.splitext(archive_filename)[0])
                                            run('mkdir -p {}'.format(release_path))
                                                run('tar -xzf /tmp/{} -C {}'.format(archive_filename, release_path))
                                                    
                                                        # Delete the archive from the web servers
                                                            run('rm /tmp/{}'.format(archive_filename))
                                                                
                                                                    # Delete the symbolic link /data/web_static/current from the web servers
                                                                        run('rm /data/web_static/current')
                                                                            
                                                                                # Create a new symbolic link /data/web_static/current on the web servers
                                                                                    run('ln -s {} /data/web_static/current'.format(release_path))
                                                                                        
                                                                                            return True

