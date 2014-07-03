#!/bin/sh
#
# --> WinSOL init.d scripts (create with skeletor.)
#   

PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
DAEMON="/usr/share/winsol/web/web_winsol.py"
NAME="winsol"
DESC="WinSOL Web Interface daemon service"

set -e

case "$1" in
  start)
	echo -n "Starting $DESC: "
	start-stop-daemon --start --quiet --background -m --pidfile /var/run/$NAME.pid --exec $DAEMON  
	echo "$NAME."
	;;
  stop)
	echo -n "Stopping $DESC: "
        start-stop-daemon --stop --pidfile /var/run/$NAME.pid 
	echo "$NAME."
	;;
  restart)
        echo -n "Stopping $DESC: "
	start-stop-daemon --stop --pidfile /var/run/$NAME.pid 
	echo "$NAME."

        echo -n "Starting $DESC: "
        start-stop-daemon --start --quiet --background -m --pidfile /var/run/$NAME.pid --exec $DAEMON 
        echo "$NAME."
        ;;
  *)
	N=/etc/init.d/$NAME
	# echo "Usage: $N {start|stop|restart|reload|force-reload}" >&2
	echo "Usage: $N {start|stop|restart}" >&2
	exit 1
	;;
esac

exit 0
