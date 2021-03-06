# Docker file for pfdorun_mriconvert ChRIS plugin app
#
# Build with
#
#   docker build -t <name> .
#
# For example if building a local version, you could do:
#
#   docker build -t local/pl-pfdorun_mriconvert .
#
# In the case of a proxy (located at 192.168.13.14:3128), do:
#
#    docker build --build-arg http_proxy=http://192.168.13.14:3128 --build-arg UID=$UID -t local/pl-pfdorun_mriconvert .
#
# To run an interactive shell inside this container, do:
#
#   docker run -ti --entrypoint /bin/bash local/pl-pfdorun_mriconvert
#
# To pass an env var HOST_IP to container, do:
#
#   docker run -ti -e HOST_IP=$(ip route | grep -v docker | awk '{if(NF==11) print $9}') --entrypoint /bin/bash local/pl-pfdorun_mriconvert
#

FROM python:3.9.1-slim-buster
LABEL maintainer="Arushi Vyas <dev@babyMRI.org>"

WORKDIR /usr/local/src

COPY requirements.txt .
COPY mri_convert .
COPY license.txt .
COPY FreeSurferColorLUT.txt .
COPY ["mri_convert", "/usr/bin/"]
RUN pip install -r requirements.txt \
    && apt-get update \
    && apt-get install libgomp1 \
    && rm -rf /var/lib/apt/lists/*

COPY . .
RUN pip install .

ENV PATH="/usr/local/freesurfer/bin:/usr/local/freesurfer/fsfast/bin:/usr/local/freesurfer/tktools:/usr/local/freesurfer/mni/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:" \
    FREESURFER_HOME="/usr/local/freesurfer" \
    SUBJECTS_DIR="/outgoing" \
    MINC_LIB_DIR="/usr/local/freesurfer/mni/lib" \
    MNI_DATAPATH="/usr/local/freesurfer/mni/data" \
    PERL5LIB="/usr/local/freesurfer/mni/share/perl5" \
    MINC_BIN_DIR="/usr/local/freesurfer/mni/bin" \
    MNI_PERL5LIB="/usr/local/freesurfer/mni/share/perl5" \
    FMRI_ANALYSIS_DIR="/usr/local/freesurfer/fsfast" \
    FUNCTIONALS_DIR="/usr/local/freesurfer/sessions" \
    LOCAL_DIR="/usr/local/freesurfer/local" \
    FSFAST_HOME="/usr/local/freesurfer/fsfast" \
    MNI_DIR="/usr/local/freesurfer/mni" \
    FSF_OUTPUT_FORMAT="nii.gz"

CMD ["pfdorun_mriconvert", "--help"]
