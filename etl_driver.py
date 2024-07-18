from extract import Extract
from transform import Transform
from load import Load


class Driver():
    def __init__( self ):
        super().__init__();

    def run_extract( self ):
        # run extract
        self.extract_obj = Extract(wearable="whoop");
        self.extract_response = self.extract_obj.main(api="profile");
        print( self.extract_response );
    
    def run_transform( self ):
        # run transform
        self.transform_obj = Transform( self.extract_response );
        self.transform_response = self.transform_obj.transform();
        print( self.transform_response );
    
    def run_load( self ):
        # run load
        self.load_obj = Load();
        self.load_obj.df( self.transform_response, "profile" );

    def main( self ):
        self.run_extract();
        self.run_transform();
        self.run_load();

if __name__ == "__main__":
    driver = Driver();
    driver.main();