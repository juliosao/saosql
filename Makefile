TARGET=saosql
VERSION=$(shell awk '/Version:/ { print $$2 }' pkg/$(TARGET).spec)
DIST=ui py extras pkg Makefile

all: py/*.py
	python -m compileall py

$(TARGET)-$(VERSION).tar.bz2: clean	
	mkdir $(TARGET)-$(VERSION)
	cp -rf $(DIST) $(TARGET)-$(VERSION)
	tar cvjf $(TARGET)-$(VERSION).tar.bz2 $(TARGET)-$(VERSION)
	rm -rf $(TARGET)-$(VERSION)

rpm: dist
	rpmbuild -tb $(TARGET)-$(VERSION).tar.bz2

deb: clean
	mkdir $(TARGET)-$(VERSION)
	make install PREFIX=$(TARGET)-$(VERSION)
	cp -rf pkg/DEBIAN $(TARGET)-$(VERSION)
	sed -i "s/VERSION/$(VERSION)/g" $(TARGET)-$(VERSION)/DEBIAN/control
	dpkg-deb --build $(TARGET)-$(VERSION)

.phony: clean dist install

install:
	mkdir -p $(PREFIX)/opt/saosql/ui $(PREFIX)/opt/saosql/py $(PREFIX)/opt/saosql/extras
	install -m 555 py/*.py $(PREFIX)/opt/saosql/py
	install -m 444 ui/*.glade $(PREFIX)/opt/saosql/ui
	install -m 444 extras/* $(PREFIX)/opt/saosql/extras
	chmod +x $(PREFIX)/opt/saosql/extras/*.sh
	mkdir -p $(PREFIX)/usr/bin
	ln -s /opt/saosql/extras/launcher.sh $(PREFIX)/usr/bin/saosql
	mkdir -p $(PREFIX)/usr/share/applications
	cp extras/sao-saosql.desktop $(PREFIX)/usr/share/applications	

dist: $(TARGET)-$(VERSION).tar.bz2

clean:
	-find . -name '*.pyc' | xargs rm -f
	-rm -f *.tar.bz2
	-rm -rf $(TARGET)-$(VERSION)
