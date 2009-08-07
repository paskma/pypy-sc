package pypy;

class SimpleLock
    {
        boolean locked;
        public SimpleLock()
        {
            locked = false;
        }

        public synchronized void acquire()
        {
            while (locked)
            {
                try
                {
                    wait();
                }
                catch(InterruptedException ex)
                {
                    System.out.println(ex.toString());
                    throw new RuntimeException(ex);
                }
            }
            locked = true;
        }

        public synchronized void release()
        {
            locked = false;
            notify();
        }
    }