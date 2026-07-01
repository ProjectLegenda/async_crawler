import subprocess

subprocess.call(f'''hadoop distcp -Dmapreduce.job.hdfs-servers.token-renewal.exclude=\
                    cpks05hdgm01r.rxcorp.com,cpks06hdgm01r.rxcorp.com\
					-D ipc.client.fallback-to-simple-auth-allowed=true\
					-Dmapred.job.queue.name=sts -skipcrccheck\
					-update hdfs://cpks05hdgm01r.rxcorp.com:8020/user/dyao/.vimrc\
					hdfs://cdts01hdfm01p.rxcorp.com:8020/user/dyao/''', shell=True)
