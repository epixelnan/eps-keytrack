PASSGEN=$$(uuid|sha512sum|cut -f 1 -d ' ')
env-files:
	if [ ! -f .env ]; then echo "REDIS_PASSWORD=$(PASSGEN)" > .env; fi
	mkdir -p env
	if [ ! -f env/db.secret.env ]; then echo "POSTGRES_PASSWORD=$(PASSGEN)" > env/db.secret.env; fi
	if [ ! -f env/db.env ]; then \
		echo "POSTGRES_NAME=postgres" >  env/db.env; \
		echo "POSTGRES_USER=postgres" >> env/db.env; \
	fi
	if [ ! -f env/dj.secret.env ]; then echo "EPS_DJ_SECRET_KEY=$(PASSGEN)" > env/dj.secret.env; fi

settings:
	if [ ! -f keytrack/settings_private.py ]; then \
		cp keytrack/settings_private.sample.py keytrack/settings_private.py; \
	fi
	
	if [ ! -f keytrack/settings_secret.py ]; then \
		cp keytrack/settings_secret.sample.py keytrack/settings_secret.py; \
	fi
