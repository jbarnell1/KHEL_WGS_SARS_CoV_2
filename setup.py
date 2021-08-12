from distutils.core import setup

setup(name='KHEL Molecular Genomics (Jonathan Barnell',
    version='1.0',
    description='Aid for daily WGS SARS CoV 2 Workflow',
    author='Jonathan Barnell',
    author_email='KDHE.MolecularGenomics@ks.gov',
    url='https://github.com/jbarnell1/KHEL_WGS_SARS_CoV_2',
    packages=['pandas', 'numpy', 'sqlalchemy',
        'tk', 'cx_oracle', 'paramiko'],
    platforms=['Windows 10 64-bit'],
    )