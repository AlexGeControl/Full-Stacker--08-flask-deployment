import os
import sys
import click

from application import create_app

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

# coverage analysis engine:
cov = None
if os.environ.get('FLASK_COVERAGE'):
    import coverage    
    cov = coverage.coverage(branch=True, include='application/*')    
    cov.start()

# flask unittests:
@app.cli.command()
@click.option(
    '--coverage', default=False,
    help='Run tests under code coverage.'
)
def test(coverage):    
    """ Run the unit tests.
    """    
    # if coverage analysis is needed but the engine is not launched, re-run the command
    if coverage and not os.environ.get('FLASK_COVERAGE'):        
        os.environ['FLASK_COVERAGE'] = 'true'        
        os.execvp(sys.executable, [sys.executable] + sys.argv)    
    
    import unittest    
    
    tests = unittest.TestLoader().discover('tests')    
    unittest.TextTestRunner(verbosity=2).run(tests)    
    
    if cov:
        cov.stop()        
        cov.save()        
        # summary:
        print('Coverage Summary:')        
        cov.report()        
        # detailed report in HTML:
        basedir = os.path.abspath(os.path.dirname(__file__))        
        covdir = os.path.join(basedir, 'coverage')        
        cov.html_report(directory=covdir)        
        print('Detailed report in HTML is available at: file://%s/index.html' % covdir)
        # close:        
        cov.erase()
