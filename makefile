server: main.c ./include/threadpool.h ./include/http_conn.cpp ./include/http_conn.h ./include/locker.h ./include/log.cpp ./include/log.h ./include/block_queue.h ./include/CGI/mysql_conn_pool.cpp ./include/CGI/mysql_conn_pool.h
	g++ -o server main.c ./include/threadpool.h ./include/http_conn.cpp ./include/http_conn.h ./include/locker.h ./include/log.cpp ./include/log.h ./include/block_queue.h ./include/CGI/mysql_conn_pool.cpp ./include/CGI/mysql_conn_pool.h -lpthread -lmysqlclient


clean:
	rm  -r server