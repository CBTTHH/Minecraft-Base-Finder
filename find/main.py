import minescript as m
import find.core.python.scanning as scanning
import find.core.python.filtering as filtering
import find.core.python.converter as converter
import find.config.constants as C

def main():
    block_regions = scanning.scan(C.Y_LEVEL_SEARCHING_SURFACE_TH, C.Y_LEVEL_SEARCHING_SKY_TH, C.Y_LEVEL_SEARCHING_UNDERGROUND_TH)
    interesting_blocks = filtering.filter_regions(block_regions)
    converter.to_json(interesting_blocks)
    
if __name__ == "__main__":
    main()

