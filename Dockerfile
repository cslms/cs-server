FROM pythonboilerplate/python3:webdev


# Install apt dependencies

RUN apt-get update &&\
    apt-get install --no-install-recommends --no-install-suggests -y \
    \
    # Scientific python stack for plots
            python3-numpy \
            python3-matplotlib \
            python3-pandas \
            python3-dev \
            python3-lxml \
    \
    # Compilers and languages for the e-judge
            build-essential \
            gcc \
            g++ \
            tcc \
            ruby \
            python \
            python-pip \
    \
    # Useful tooling
            nano \
    \
    # Python deps available in apt-get
            python3-markdown \
            python3-html5lib \
            python3-bleach \
            python3-virtualenv \
    \
    # Extra deps
            python3-pillow \
            python3-psutil \
            python3-pexpect

# Install important deps with pip. This prevents hitting cache too frequently
# due to changes in the package dependencies.

RUN pip3 install \
            rcssmin &&\
    \
    pip3 install \
    # Base deps
            lazyutils \
            Markdown \
            mistune \
            PyYAML \
            fake-factory \
            factory-boy \
            mommys_boy \
            python-social-auth \
            pygments \
            html5lib \
            bleach \
            pygeneric \
    \
    # Templating
            jinja2 \
            djinga \
    \
    # E-judge support
            markio \
            iospec \
            ejudge \
            boxed \
            srvice \
   \
    # Testing
            pytest \
            pytest-factoryboy \
            pytest-selenium \
            pytest-django \
            mock \
            virtualenv \
    \
    # Django deps
            django==1.9 \
            wagtail==1.5 \
            wagtail-model-tools \
            django-model-utils \
            django-picklefield \
            django-jsonfield \
            django-annoying \
            django-activity-stream \
            django-compressor \
            django-userena \
            django-polymorphic \
            django-model-reference



# Extra dependencies for additional language support

RUN pip3 install \
            pytuga


# Install Python dependencies. The list above is just a list of deps that are
# very unlikely to change. We still have to update with the latest changes in
# requirements.txt.
# 
# It is nice to create dummy VERSION and README.rst files to prevent cache 
# misses due to trivial and unimportant changes.

COPY ["setup.py", "requirements.txt", "/app/"]
RUN echo "README" > README.rst &&\
    echo "0.1.0" > VERSION &&\
    pip3 install -e ".[dev]" -r requirements.txt &&\
    pip3 install \
            six>=1.9


# Copy files and data
# We specify each file individually and add collect files from a tar.gz

COPY [ \
#      ".coveragerc", \ 
#      ".travis.yml", \
      "boilerplate.ini", \
      "manage.py", \ 
      "package.json", \
      "pytest.ini", \
      "tasks.py", \
      "tox.ini", \
      "webpack.config.js", \
      "/app/" \
]
COPY src/ /app/src/

RUN python3 manage.py collectstatic --no-input &&\
    webpack

# Set variables and volumes

ENV WSGI_APPLICATION=codeschool.site.wsgi
VOLUME ["/app/db/", "/app/collect/media/"]

