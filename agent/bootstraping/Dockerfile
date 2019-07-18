FROM tatsushid/tinycore:7.2-x86_64

WORKDIR /app
COPY . /app

ENV LANG=C.UTF-8 LC_ALL=C

RUN tce-load -wic gnupg curl \
    && rm -rf /tmp/tce/optional/*

# gpg: key AA65421D: public key "Ned Deily (Python release signing key) <nad@python.org>" imported
RUN gpg2 --keyserver pool.sks-keyservers.net --recv-keys 0D96DF4D4110E5C43FBFB17F2D347EA6AA65421D

ENV PYTHON_VERSION 3.6.0

# if this is called "PIP_VERSION", pip explodes with "ValueError: invalid truth value '<VERSION>'"
ENV PYTHON_PIP_VERSION 9.0.1

RUN tce-load -wic \
        bzip2-dev \
        flex \
        file \
        gcc \
        make \
        linux-4.2.1_api_headers \
        glibc_add_lib \
        glibc_base-dev \
        openssl-dev \
        gdbm-dev \
        ncurses-dev \
        readline-dev \
        sqlite3-dev \
        liblzma-dev \
        zlib_base-dev \
        tk-dev \
        libX11-dev \
        libXss \
        xorg-proto \
    && cd /tmp \
    && curl -SL "https://www.python.org/ftp/python/$PYTHON_VERSION/Python-$PYTHON_VERSION.tar.xz" -o python.tar.xz \
    && curl -SL "https://www.python.org/ftp/python/$PYTHON_VERSION/Python-$PYTHON_VERSION.tar.xz.asc" -o python.tar.xz.asc \
    && gpg2 --verify python.tar.xz.asc \
    && rm python.tar.xz.asc \
    && tar -xJf python.tar.xz \
    && rm python.tar.xz \
    && cd "/tmp/Python-$PYTHON_VERSION" \
    && ./configure --enable-shared \
    && make \
    && mkdir tmp_install \
    && make install DESTDIR=tmp_install \
    && for F in `find tmp_install | xargs file | grep "executable" | grep ELF | grep "not stripped" | cut -f 1 -d :`; do \
            [ -f $F ] && strip --strip-unneeded $F; \
        done \
    && for F in `find tmp_install | xargs file | grep "shared object" | grep ELF | grep "not stripped" | cut -f 1 -d :`; do \
            [ -f $F ] && if [ ! -w $F ]; then chmod u+w $F && strip -g $F && chmod u-w $F; else strip -g $F; fi \
        done \
    && for F in `find tmp_install | xargs file | grep "current ar archive" | cut -f 1 -d :`; do \
            [ -f $F ] && strip -g $F; \
        done \
    && find tmp_install \( -type f -a -name '*.pyc' -o -name '*.pyo' \) -exec rm -rf '{}' + \
    && find tmp_install \( -type d -a -name test -o -name tests \) | xargs rm -rf \
    && $(cd tmp_install; sudo cp -R . /) \
    && rm -rf "/tmp/Python-$PYTHON_VERSION" \
    && cd /tmp/tce/optional \
    && for PKG in `ls *-dev.tcz`; do \
            echo "Removing $PKG files"; \
            for F in `unsquashfs -l $PKG | grep squashfs-root | sed -e 's/squashfs-root//'`; do \
                [ -f $F -o -L $F ] && sudo rm -f $F; \
            done; \
            INSTALLED=$(echo -n $PKG | sed -e s/.tcz//); \
            sudo rm -f /usr/local/tce.installed/$INSTALLED; \
        done \
    && for PKG in binutils.tcz \
                cloog.tcz \
                flex.tcz \
                file.tcz \
                gcc.tcz \
                gcc_libs.tcz \
                linux-4.2.1_api_headers.tcz \
                make.tcz \
                sqlite3-bin.tcz \
                xz.tcz \
                xorg-proto.tcz; do \
            echo "Removing $PKG files"; \
            for F in `unsquashfs -l $PKG | grep squashfs-root | sed -e 's/squashfs-root//'`; do \
                [ -f $F -o -L $F ] && sudo rm -f $F; \
            done; \
            INSTALLED=$(echo -n $PKG | sed -e s/.tcz//); \
            sudo rm -f /usr/local/tce.installed/$INSTALLED; \
        done \
    && sudo rm -f /usr/bin/file \
    && sudo /sbin/ldconfig \
    && rm -rf /tmp/tce/optional/* \
    && curl -SL 'https://bootstrap.pypa.io/get-pip.py' | sudo python3 \
    && sudo pip3 install --no-cache-dir --upgrade pip==$PYTHON_PIP_VERSION \
    && sudo pip3 install requests coloredlogs \
    && sudo find /usr/local \( -type f -a -name '*.pyc' -o -name '*.pyo' \) -exec rm -rf '{}' + \
    && find /usr/local \( -type d -a -name test -o -name tests \) | sudo xargs rm -rf \
    && sudo rm -rf /usr/src/python

# Instructions after here are run with 'root' user
USER root

RUN cd /usr/local/bin \
    && ln -s easy_install-3.6 easy_install \
    && ln -s idel3 idle \
    && ln -s pydoc3 pydoc \
    && ln -s python3 python \
    && ln -s python3-config python-config