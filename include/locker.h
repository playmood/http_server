#ifndef LOCKER_H
#define LOCKER_H

#include <exception>
#include <pthread.h>
#include <semaphore.h>

class sem
{
    public:
        //默认构造函数，信号量的值为0
        sem()
        {
            if(sem_init(&p_sem, 0, 0) != 0)
            {
                throw std::exception();
            }
        }
        //设定信号量的值为num
        sem(int num)
        {
            if(sem_init(&p_sem, 0, num) != 0)
            {
                throw std::exception;
            }
        }
        ~sem()
        {
            sem_destroy(&p_sem);
        }
        bool wait()
        {
            return sem_wait(&p_sem) == 0;
        }
        bool post()
        {
            return sem_post(&p_sem) == 0;
        }


    private:
        sem_t p_sem;
};

class locker
{
    public:
        locker()
        {
            if(pthread_mutex_init(&p_mutex, NULL) != 0)
            {
                throw std::exception();
            }

        }
        ~locker()
        {
            pthread_mutex_destroy(&p_mutex);
        }
        bool lock()
        {
            return pthread_mutex_lock(&p_mutex) == 0;
        }
        bool unlock()
        {
            return pthread_mutex_unlock(&p_mutex) == 0;
        }
        pthread_mutex_t *get()
        {
            return &p_mutex;
        }

    private:
        pthread_mutex_t p_mutex;
};

class cond
{
    public:
        cond()
        {
            if(pthread_cond_init(&p_cond, NULL) != 0)
            {
                //pthread_mutex_destroy(&p_mutex);
                throw std::exception();
            }
        }
        ~cond()
        {
            pthread_cond_destroy(&p_cond);
        }
        bool wait(pthread_cond_t *p_mutex)
        {
            int ret = 0;
            //pthread_mutex_lock(&p_mutex);
            ret = pthread_cond_wait(&p_cond, p_mutex);
            //pthread_mutex_unlock(&p_mutex);
            return ret == 0; 
        }
        bool timewait(pthread_mutex_t *p_mutex, struct timespec t)
        {
            int ret = 0;
            //pthread_mutex_lock(&p_mutex);
            ret = pthread_cond_timedwait(&p_cond, p_mutex, &t);
            //pthread_mutex_unlock(&p_mutex);
            return ret == 0;
        }
        bool signal()
        {
            return pthread_cond_signal(&p_cond) == 0;
        }
        bool broadcast()
        {
            return pthread_cond_broadcast(&p_cond) == 0;
        }
    
    private:
        pthread_cond_t p_cond;
        //static pthread_mutex_t p_mutex;
};



#endif