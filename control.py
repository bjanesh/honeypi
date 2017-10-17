import os
import sys
import serial

class Autostar():
    def __init__(self):
        self.port = serial.Serial(
            port='/dev/ttyAMA0',
            baudrate = 9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
        )
        
    # ACK - Alignment Query
    def alignment_query(self):
        self.port.write('0x06')
        response = self.port.readline()
        assert response in ['A', 'L', 'P']
        return response
    # ACK <0x06> Query of alignment mounting mode. Returns:
    # A If scope in AltAz Mode / L If scope in Land Mode / P If scope in Polar Mode


    # A - Alignment Commands
    def align_auto(self):
        self.port.write(':Aa#')
        response = self.port.readline()
        return response
    # :Aa# Start Telescope Automatic Alignment Sequence [LX200GPS only] Returns:
    # 1: When complete (can take several minutes). 0: If scope not AzEl Mounted or align fails
    
    def align_land(self):
        self.port.write(':AL#')
        response = self.port.readline()
        return response
    # :AL# Sets telescope to Land alignment mode Returns: nothing
    
    def align_polar(self):
        self.port.write(':AP#')
        response = self.port.readline()
        return response
    # :AP# Sets telescope to Polar alignment mode Returns: nothing
    
    def align_altaz(self):
        self.port.write(':AA#')
        response = self.port.readline()
        return response
    # :AA# Sets telescope the AltAz alignment mode Returns: nothing


    # $B – Active Backlash Compensation
    def antibacklash_alt(self, value):
        self.port.write(':$BA{:2d}#'.format(value))
        response = self.port.readline()
        return response
    # :$BAdd#
    # Set Altitude/Dec Antibacklash
    # Returns Nothing
    
    def antibacklash_az(self, value):
        self.port.write(':$BZ{:2d}#'.format(value))
        response = self.port.readline()
        return response
    # :$BZdd#
    # Set Azimuth/RA Antibacklash
    # Returns Nothing


    # B - Reticule/Accessory Control
    def reticule_brightness_inc(self):
        self.port.write(':B+#')
        response = self.port.readline()
        return response
    # :B+# Increase reticule Brightness Return: Nothing
    
    def reticule_brightness_dec(self):
        self.port.write(':B-#')
        response = self.port.readline()
        return response
    # :B-# Decrease Reticule Brightness Return: Nothing
    
    def set_reticule_flash_rate(self, value):
        assert value in [0,1,2,3,4,5,6,7,8,9]
        self.port.write(':B{:1d}#'.format(value))
        response = self.port.readline()
        return response
    # :B<n># Set Reticle flash rate to <n> (an ASCII expressed number) <n> Values of 0..3 for LX200 series
    # <n> Values of 0..9 for Autostar and LX200GPS Return: Nothing
    
    def set_reticule_flash_cycle(self, value):
        # self.port.write(':T+#')
        response = self.port.readline()
        return response
    # :BDn# Set Reticule Duty flash duty cycle to <n> (an ASCII expressed digit) [LX200 GPS Only] 
    # <n> Values: 0 = On, 1..15 flash rate
    # Return: Nothing


    # C - Sync Control
    def sync_selenographic(self):
        self.port.write(':CL#')
        response = self.port.readline()
        return response
    # :CL# Synchonize the telescope with the current Selenographic coordinates.
    
    def sync_object(self):
        self.port.write(':CM#')
        response = self.port.readline()
        return response
    # :CM# Synchronizes the telescope's position with the currently selected database object's coordinates. Returns:
    # LX200's - a "#" terminated string with the name of the object that was synced. Autostars & LX200GPS - At static string: " M31 EX GAL MAG 3.5 SZ178.0'#"


    # D - Distnace Bars
    def get_distance_bars(self):
        self.port.write(':D#')
        response = self.port.readline()
        return response
    # :D# Requests a string of bars indicating the distance to the current library object. Returns:
    # LX200's – a string of bar characters indicating the distance.
    # Autostars and LX200GPS – a string containing one bar until a slew is complete, then a null string is returned.


    # f - Fan Command
    def fan_on(self):
        self.port.write(':f+#')
        response = self.port.readline()
        return response
    # :f+# 
    # LX 16”– Turn on the tube exhaust fan 
    # LX200GPS – Turn on power to accessor panel 
    # Autostar & LX200 < 16” – Not Supported 
    # Returns: nothing
    
    def fan_off(self):
        self.port.write(':f-#')
        response = self.port.readline()
        return response
    # :f-# 
    # LX 16”– Turn off tube exhaust fan
    # LX200GPS - Turn off power to accessory panel 
    # Autostar & LX200 < 16” – Not Supported 
    # Returns: Nothing
    
    def get_tube_temp(self):
        self.port.write(':fT#')
        response = self.port.readline()
        return response
    # :fT# 
    # LX200GPS – Return Optical Tube Assembly Temperature
    # Returns <sdd.ddd># - a ‘#’ terminated signed ASCII real number indicating the Celsius ambient temperature. 
    # All others – Not supported


    # F – Focuser Control
    def focus_in(self):
        self.port.write(':F+#')
        response = self.port.readline()
        return response
    # :F+# Start Focuser moving inward (toward objective) Returns: None
    
    def focus_out(self):
        self.port.write(':F-#')
        response = self.port.readline()
        return response
    # :F-# Start Focuser moving outward (away from objective) Returns: None
    
    def focus_stop(self):
        self.port.write(':FQ#')
        response = self.port.readline()
        return response
    # :FQ# Halt Focuser Motion Returns: Notrhing
    
    def set_focus_fast(self):
        self.port.write(':FF#')
        response = self.port.readline()
        return response
    # :FF# Set Focus speed to fastest setting Returns: Nothing
    
    def set_fcous_slow(self):
        self.port.write(':FS#')
        response = self.port.readline()
        return response
    # :FS# Set Focus speed to slowest setting Returns: Nothing
    
    def set_focus_speed(self, value):
        assert value in [1,2,3,4]
        self.port.write(':F{:1d}#'.format(value))
        response = self.port.readline()
        return response
    # :F<n># Autostar & LX200GPS – set focuser speed to <n> where <n> is an ASCII digit 1..4 Returns: Nothing
    # LX200 – Not Supported

    
    # g – GPS/Magnetometer commands
    
    # :g+# LX200GPS Only - Turn on GPS Returns: Nothing
    
    # :g-# LX200GPS Only - Turn off GPS
    
    # :gps# LX200GPS Only – Turns on NMEA GPS data stream.
    # Returns: The next string from the GPS in standard NEMA format followed by a ‘#’ key
    
    # :gT# Powers up the GPS and updates the system time from the GPS stream. The process my take several minutes to complete. During GPS update, normal handbox operations are interrupted. [LX200gps only]
    # Returns: ‘0’ In the event that the user interrupts the process, or the GPS times out.
    # Returns: ‘1’ After successful updates


    # G – Get Telescope Information
    def get_align0(self):
        self.port.write(':G0#')
        response = self.port.readline()
        return response
    # :G0# Get Alignment Menu Entry 0
    # Returns: A ‘#’ Terminated ASCII string. [LX200 legacy command]
    
    def get_align1(self):
        self.port.write(':G1#')
        response = self.port.readline()
        return response
    # :G1# Get Alignment Menu Entry 0
    # Returns: A ‘#’ Terminated ASCII string. [LX200 legacy command]
    
    def get_align2(self):
        self.port.write(':G2#')
        response = self.port.readline()
        return response
    # :G2# Get Alignment Menu Entry 0
    # Returns: A ‘#’ Terminated ASCII string. [LX200 legacy command]
    
    def get_tel_alt(self):
        self.port.write(':GA#')
        response = self.port.readline()
        return response
    # :GA# Get Telescope Altitude
    # Returns: sDD*MM# or sDD*MM’SS#
    # The current scope altitude. The returned format depending on the current precision setting.
    
    def get_lt12(self):
        self.port.write(':Ga#')
        response = self.port.readline()
        return response
    # :Ga# Get Local Telescope Time In 12 Hour Format Returns: HH:MM:SS#
    # The time in 12 format
    
    def get_mag_bright_lim(self):
        self.port.write(':Gb#')
        response = self.port.readline()
        return response
    # :Gb# Get Browse Brighter Magnitude Limit Returns: sMM.M#
    # The magnitude of the faintest object to be returned from the telescope FIND/BROWSE command. Command when searching for objects in the Deep Sky database.
    
    def get_date(self):
        self.port.write(':GC#')
        response = self.port.readline()
        return response
    # :GC# Get current date. Returns: MM/DD/YY#
    # The current local calendar date for the telescope.
    
    def get_cal_format(self):
        self.port.write(':Gc#')
        response = self.port.readline()
        return response
    # :Gc# Get Calendar Format Returns: 12# or 24#
    # Depending on the current telescope format setting.
    
    def get_telescope_dec(self):
        self.port.write(':GD#')
        response = self.port.readline()
        return response
    # :GD# Get Telescope Declination.
    # Returns: sDD*MM# or sDD*MM’SS#
    # Depending upon the current precision setting for the telescope.
    
    def get_obj_dec(self):
        self.port.write(':Gd#')
        response = self.port.readline()
        return response
    # :Gd# Get Currently Selected Object/Target Declination Returns: sDD*MM# or sDD*MM’SS#
    # Depending upon the current precision setting for the telescope.
    
    def get_field_diameter(self):
        self.port.write(':GF#')
        response = self.port.readline()
        return response
    # :GF# Get Find Field Diameter Returns: NNN#
    # An ASCIi interger expressing the diameter of the field search used in the IDENTIFY/FIND commands.
    
    def get_mag_faint_lim(self):
        self.port.write(':Gf#')
        response = self.port.readline()
        return response
    # :Gf# Get Browse Faint Magnitude Limit Returns: sMM.M#
    # The magnitude or the birghtest object to be returned from the telescope FIND/BROWSE command.
    
    def get_utc_offset(self):
        self.port.write(':GG#')
        response = self.port.readline()
        return response
    # :GG# Get UTC offset time Returns: sHH# or sHH.H#
    # The number of decimal hours to add to local time to convert it to UTC. If the number is a whole number the sHH# form is returned, otherwise the longer form is return. On Autostar and LX200GPS, the daylight savings setting in effect is factored into returned value.
    
    def get_site_long(self):
        self.port.write(':Gg#')
        response = self.port.readline()
        return response
    # :Gg# Get Current Site Longitude Returns: sDDD*MM#
    # The current site Longitude. East Longitudes are expressed as negative
    
    def get_high_lim(self):
        self.port.write(':Gh#')
        response = self.port.readline()
        return response
    # :Gh# Get High Limit Returns: sDD*
    # The minimum elevation of an object above the horizon to which the telescope will slew with reporting a “Below Horizon” error.
    
    def get_lt24(self):
        self.port.write(':GL#')
        response = self.port.readline()
        return response
    # :GL# Get Local Time in 24 hour format Returns: HH:MM:SS#
    # The Local Time in 24-hour Format
    
    def get_size_large_lim(self):
        self.port.write(':Gl#')
        response = self.port.readline()
        return response
    # :Gl# Get Larger Size Limit Returns: NNN’#
    # The size of the smallest object to be returned by a search of the telescope using the BROWSE/FIND commands.
    
    def get_site_name1(self):
        self.port.write(':GM#')
        response = self.port.readline()
        return response
    # :GM# Get Site 1 Name Returns: <string>#
    # A ‘#’ terminated string with the name of the requested site.
    
    def get_site_name2(self):
        self.port.write(':GN#')
        response = self.port.readline()
        return response
    # :GN# Get Site 2 Name Returns: <string>#
    # A ‘#’ terminated string with the name of the requested site.
    
    def get_site_name3(self):
        self.port.write(':GO#')
        response = self.port.readline()
        return response
    # :GO# Get Site 3 Name Returns: <string>#
    # A ‘#’ terminated string with the name of the requested site.
    
    def get_site_name4(self):
        self.port.write(':GP#')
        response = self.port.readline()
        return response
    # :GP# Get Site 4 Name Returns: <string>#
    # A ‘#’ terminated string with the name of the requested site.
    
    def get_low_lim(self):
        self.port.write(':Go#')
        response = self.port.readline()
        return response
    # :Go# Get Lower Limit Returns: DD*#
    # The highest elevation above the horizon that the telescope will be allowed to slew to without a warning message.
    
    def get_quality_min(self):
        self.port.write(':Gq#')
        response = self.port.readline()
        return response
    # :Gq# Get Minimum Quality For Find Operation Returns:
    # SU# Super
    # EX# Excellent
    # VG# Very Good
    # GD# Good
    # FR# Fair
    # PR# Poor
    # VP# Very Poor
    # The mimum quality of object returned by the FIND command.
    
    def get_tel_ra(self):
        self.port.write(':GR#')
        response = self.port.readline()
        return response
    # :GR# Get Telescope RA
    # Returns: HH:MM.T# or HH:MM:SS#
    # Depending which precision is set for the telescope
    
    def get_obj_ra(self):
        self.port.write(':Gr#')
        response = self.port.readline()
        return response
    # :Gr# Get current/target object RA Returns: HH:MM.T# or HH:MM:SS
    # Depending upon which precision is set for the telescope
    
    def get_lst(self):
        self.port.write(':GS#')
        response = self.port.readline()
        return response
    # :GS# Get the Sidereal Time Returns: HH:MM:SS#
    # The Sidereal Time as an ASCII Sexidecimal value in 24 hour format
    
    def get_size_small_lim(self):
        self.port.write(':Gs#')
        response = self.port.readline()
        return response
    # :Gs# Get Smaller Size Limit Returns: NNN'#
    # The size of the largest object returned by the FIND command expressed in arcminutes.
    
    def get_tracking_rate(self):
        self.port.write(':GT#')
        response = self.port.readline()
        return response
    # :GT# Get tracking rate Returns: TT.T#
    # Current Track Frequency expressed in hertz assuming a synchonous motor design where a 60.0 Hz motor clock would produce 1 revolution of the telescope in 24 hours.
    
    def get_site_lat(self):
        self.port.write(':Gt#')
        response = self.port.readline()
        return response
    # :Gt# Get Current Site Latitdue Returns: sDD*MM#
    # The latitude of the current site. Positive inplies North latitude.
    
    def get_firmware_date(self):
        self.port.write(':GVD#')
        response = self.port.readline()
        return response
    # :GVD# Get Telescope Firmware Date Returns: mmm dd yyyy#
    
    def get_firmware_num(self):
        self.port.write(':GVN#')
        response = self.port.readline()
        return response
    # :GVN# Get Telescope Firmware Number Returns: dd.d#
    
    def get_product_name(self):
        self.port.write(':GVP#')
        response = self.port.readline()
        return response
    # :GVP# Get Telescope Product Name Returns: <string>#
    
    def get_firmware_time(self):
        self.port.write(':GVT#')
        response = self.port.readline()
        return response
    # :GVT# Get Telescope Firmware Time returns: HH:MM:SS#
    
    def get_dso_string(self):
        self.port.write(':Gy#')
        response = self.port.readline()
        return response
    # :Gy# Get deepsky object search string Returns: GPDCO#
    # A string indicaing the class of objects that should be returned by the FIND/BROWSE command. If the character is upper case, the object class is return. If the character is lowercase, objects of this class are ignored. The character meanings are as follws:
    # G – Galaxies
    # P – Planetary Nebulas D – Diffuse Nebulas C – Globular Clusters O – Open Clusters
    
    def get_tel_az(self):
        self.port.write(':GZ#')
        response = self.port.readline()
        return response
    # :GZ# Get telescope azimuth
    # Returns: DDD*MM#T or DDD*MM’SS#
    # The current telescope Azimuth depending on the selected precision.


    # h – Home Position Commands
    def go_home(self):
        self.port.write(':hS#')
        response = self.port.readline()
        return response
    # :hS# LX200GPS and LX 16” Seeks Home Position and stores the encoder values from the aligned telescope at the home position in the nonvolatile memory of the scope.
    # Returns: Nothing
    # Autostar,LX200 – Ignored
    
    def home_align(self):
        self.port.write(':hF#')
        response = self.port.readline()
        return response
    # :hF# LX200GPS and LX 16” Seeks the Home Position of the scope and sets/aligns the scope based on the encoder values stored in non-volatile memory
    # Returns: Nothing
    # Autostar,LX200 - Igrnored
    
    def sleep(self):
        self.port.write(':hN#')
        response = self.port.readline()
        return response
    # :hN# LX200GPS only: Sleep Telescope. Power off motors, encoders, displays and lights. Scope remains in minimum power mode until a keystroke is received or a wake command is sent.
    
    def go_park(self):
        self.port.write(':hP#')
        response = self.port.readline()
        return response
    # :hP# Autostar, LX200GPS and LX 16”Slew to Park Position Returns: Nothing
    
    def wake(self):
        self.port.write(':hW#')
        response = self.port.readline()
        return response
    # :hW# LX200 GPS Only: Wake up sleeping telescope.
    
    def get_home_status(self):
        self.port.write(':h?#')
        response = self.port.readline()
        assert int(response) in [0,1,2]
        return response
    # :h?# Autostar, LX200GPS and LX 16” Query Home Status Returns:
    # 0 Home Search Failed
    # 1 Home Search Found
    # 2 Home Search in Progress
    # LX200 Not Supported
    
    
    # H – Time Format Command
    def toggle_time_format(self):
        self.port.write(':H#')
        response = self.port.readline()
        return response
    # :H# Toggle Between 24 and 12 hour time format Returns: Nothing
    
    
    # I – Initialize Telescope Command
    def initialize(self):
        self.port.write(':I#')
        response = self.port.readline()
        return response
    # :I# LX200 GPS Only - Causes the telescope to cease current operations and restart at its power on initialization.
    

    # L – Object Library Commands
    # NOT IMPLEMENTED -- USE OTHER TOOLS FOR LIBRARY FUNCTIONS
    
    # :LB# Find previous object and set it as the current target object. Returns: Nothing
    # LX200GPS & Autostar – Performs no function
    
    # :LCNNNN#
    # Set current target object to deep sky catalog object number NNNN Returns : Nothing
    # LX200GPS & Autostar – Implemented in later firmware revisions
    
    # :LF# Find Object using the current Size, Type, Upper limit, lower limt and Quality contraints and set it as current target object. Returns: Nothing
    # LX200GPS & Autostar – Performs no function
    
    # :Lf# Identify object in current field. Returns: <string>#
    # Where the string contains the number of objects in field & object in center field. LX200GPS & Autostar – Performs no function. Returns static string “0 - Objects found”.
    
    # :LI# Get Object Information Returns: <string>#
    # Returns a string containing the current target object’s name and object type.
    # LX200GPS & Autostar – performs no operation. Returns static description of Andromeda Galaxy.
    
    # :LMNNNN#
    # Set current target object to Messier Object NNNN, an ASCII expressed decimal number. Returns: Nothing.
    # LX200GPS and Autostar – Implemented in later versions.
    
    # :LN# Find next deep sky target object subject to the current constraints. LX200GPS & AutoStar – Performs no function
    
    # :LoD# Select deep sky Library where D specifices
    # 0 1 2 3 4 5
    # 1
    # 0
    # LX200GPS & AutoStar – Performs no function always returns “1”
    
    # :LsD# Select star catalog D, an ASCII integer where D specifies:
    # 0 STAR library (Not supported on Autostar I & II)
    # 1 SAO library
    # 2 GCVS library
    # Returns:
    # - Objects CNGC / NGC in Autostar & LX200GPS - Objects IC
    # – UGC
    # – Caldwell
    # – Arp – Abell
    # (Autostar & LX200GPS) (LX200 GPS)
    # (LX200 GPS)
    # Catalog available
    # Catalog Not found
    # 3 4 5
    # 1 2
    # LX200GPS & AutoStar – Available in later firmwares


    # M – Telescope Movement Commands
    def slew_to_altaz(self):
        self.port.write(':MA#')
        response = self.port.readline()
        return response
    # :MA# Autostar, LX 16”, LX200GPS – Slew to target Alt and Az 
    # Returns:
    # 0 - No fault
    # 1 – Fault
    # LX200 – Not supported
    
    def slew_east(self):
        self.port.write(':Me#')
        response = self.port.readline()
        return response
    # :Me# Move Telescope East at current slew rate Returns: Nothing
    
    def slew_north(self):
        self.port.write(':Mn#')
        response = self.port.readline()
        return response
    # :Mn# Move Telescope North at current slew rate Returns: Nothing
    
    def slew_south(self):
        self.port.write(':Ms#')
        response = self.port.readline()
        return response
    # :Ms# Move Telescope South at current slew rate Returns: Nothing
    
    def slew_west(self):
        self.port.write(':Mw#')
        response = self.port.readline()
        return response
    # :Mw# Move Telescope West at current slew rate Returns: Nothing
    
    def slew_to_obj(self):
        self.port.write(':MS#')
        response = self.port.readline()
        return response
    # :MS# Slew to Target Object 
    # Returns:
    # 0 Slew is Possible
    # 1<string># Object Below Horizon w/string message 
    # 2<string># Object Below Higher w/string message


    # P - High Precision Toggle
    def toggle_precision(self):
        self.port.write(':P#')
        response = self.port.readline()
        return response
    # :P
    # Toggles High Precsion Pointing. When High precision pointing is enabled scope will first allow the operator to center a nearby bright star before moving to the actual taget.
    # Returns: <string>
    # “HIGH PRECISION” Current setting after this command. “LOW PRECISION” Current setting after this command.
    
    
    # $Q – Smart Drive Control
    def toggle_pec(self):
        self.port.write(':$Q#')
        response = self.port.readline()
        return response
    # $Q# Toggles Smart Drive PEC on and off for both axis Returns: Nothing
    # Not supported on Autostar
    
    def enable_pec_dec(self):
        self.port.write(':$QA+#')
        response = self.port.readline()
        return response
    # :$QA+ Enable Dec/Alt PEC [LX200gps only] Returns: Nothing
    
    def disable_pec_dec(self):
        self.port.write(':$QA-#')
        response = self.port.readline()
        return response
    # :$QA- Enable Dec/Alt PEC [LX200gps only] Returns: Nothing
    
    def enable_pec_ra(self):
        self.port.write(':$QZ+#')
        response = self.port.readline()
        return response
    # :$QZ+ Enable RA/AZ PEC compensation [LX200gps only]
    # Returns: Nothing
    
    def disable_pec_ra(self):
        self.port.write(':$QZ-#')
        response = self.port.readline()
        return response
    # :$QZ- Disable RA/AZ PEC Compensation [LX200gpgs only] Return: Nothing
    
    
    # Q – Movement Commands
    def halt_all(self):
        self.port.write(':Q#')
        response = self.port.readline()
        return response
    # :Q# Halt all current slewing Returns:Nothing
    
    def halt_east(self):
        self.port.write(':Qe#')
        response = self.port.readline()
        return response
    # :Qe# Halt eastward Slews Returns: Nothing
    
    def halt_north(self):
        self.port.write(':Qn#')
        response = self.port.readline()
        return response
    # :Qn# Halt northward Slews Returns: Nothing
    
    def halt_south(self):
        self.port.write(':Qs#')
        response = self.port.readline()
        return response
    # :Qs# Halt southward Slews Returns: Nothing
    
    def halt_west(self):
        self.port.write(':Qw#')
        response = self.port.readline()
        return response
    # :Qw# Halt westward Slews Returns: Nothing
    
    
    # r – Field Derotator Commands
    
    def derotate_on(self):
        self.port.write(':r+#')
        response = self.port.readline()
        return response
    # :r+# Turn on Field Derotator [LX 16” and LX200GPS] Returns: Nothing
    
    def derotate_off(self):
        self.port.write(':r-#')
        response = self.port.readline()
        return response
    # :r-# Turn off Field Derotator, halt slew in progress. [Lx 16” and LX200GPS] Returns Nothing
    
    
    # R – Slew Rate Commands
    def set_slew_rate_center(self):
        self.port.write(':RC#')
        response = self.port.readline()
        return response
    # :RC# Set Slew rate to Centering rate (2nd slowest) Returns: Nothing
    
    def set_slew_rate_min(self):
        self.port.write(':RG#')
        response = self.port.readline()
        return response
    # :RG# Set Slew rate to Guiding Rate (slowest) Returns: Nothing
    
    def set_slew_rate_find(self):
        self.port.write(':RM#')
        response = self.port.readline()
        return response
    # :RM# Set Slew rate to Find Rate (2nd Fastest) Returns: Nothing
    
    def set_slew_rate_max(self):
        self.port.write(':RS#')
        response = self.port.readline()
        return response
    # :RS# Set Slew rate to max (fastest) Returns: Nothing
    
    def set_slew_rate_ra(self, value):
        assert value > 0.0
        self.port.write(':RA{:4.1f}#'.format(value))
        response = self.port.readline()
        return response
    # :RADD.D#
    # Set RA/Azimuth Slew rate to DD.D degrees per second [LX200GPS Only] Returns: Nothing
    
    def set_slew_rate_dec(self, value):
        assert value > 0.0
        self.port.write(':RE{:4.1f}#'.format(value))
        response = self.port.readline()
        return response
    # :REDD.D#
    # Set Dec/Elevation Slew rate to DD.D degrees per second [ LX200GPS only] Returns: Nothing
    
    def set_guide_rate(self, value):
        assert value < 15.0
        self.port.write(':Rg{:4.1f}#'.format(value))
        response = self.port.readline()
        return response
    # :RgSS.S#
    # Set guide rate to +/- SS.S to arc seconds per second. This rate is added to or subtracted from the current tracking
    # Rates when the CCD guider or handbox guider buttons are pressed when the guide rate is selected. Rate shall not exceed sidereal speed (approx 15.0417”/sec)[ LX200GPS only]
    # Returns: Nothing
    
    
    # S – Telescope Set Commands
    def set_target_alt(self, dd, mm, ss):
        self.port.write(':MS#')
        response = self.port.readline()
        return response
    # :SasDD*MM#
    # Set target object altitude to sDD*MM# or sDD*MM’SS# [LX 16”, Autostar, LX200GPS] Returns:
    # 0 Object within slew range 1 Object out of slew range
    
    def set_bright_limit(self, mag):
        self.port.write(':MS#')
        response = self.port.readline()
        return response
    # :SbsMM.M#
    # Set Brighter limit to the ASCII decimal magnitude string. SMM.M Returns:
    # 0 - Valid
    # 1 – invalid number
    
    def set_baud_rate(self, value):
        assert value in range(1,10)
        self.port.write(':MS#')
        response = self.port.readline()
        return response
    # :SBn# Set Baud Rate n, where n is an ASCII digit (1..9) with the following interpertation
    # 1     2     3     4     5     6    7    8    9
    # 56.7K 38.4K 28.8K 19.2K 14.4K 9600 4800 2400 1200
    # At the current baud rate and then changes to the new rate for further communication
    # Returns:
    # 1
    
    def set_date(self, mm, dd, yy):
        self.port.write(':MS#')
        response = self.port.readline()
        return response
    # :SCMM/DD/YY#
    # Change Handbox Date to MM/DD/YY Returns: <D><string>
    # D = ‘0’ if the date is invalid. The string is the null string.
    # D = ‘1’ for valid dates and the string is “Updating Planetary Data# #” Note: For LX200GPS this is the UTC data!
    
    def set_target_dec(self, dd, mm, ss):
        self.port.write(':MS#')
        response = self.port.readline()
        return response
    # :SdsDD*MM#
    # Set target object declination to sDD*MM or sDD*MM:SS depending on the current precision setting Returns:
    # 1 - Dec Accepted 0 – Dec invalid
    
    def set_selen_lat(self, dd, mm):
        self.port.write(':MS#')
        response = self.port.readline()
        return response
    # :SEsDD*MM#
    # Sets target object to the specificed selenographic latitude on the Moon. Returns 1- If moon is up and coordinates are accepted.
    # 0 – If the coordinates are invalid
    
    def set_selen_long(self, ddd, mm):
        self.port.write(':MS#')
        response = self.port.readline()
        return response
    # :SesDDD*MM#
    # Sets the target object to the specified selenogrphic longitude on the Moon Returns 1 – If the Moon is up and coordinates are accepted.
    # 0 – If the coordinates are invalid for any reason.
    
    def set_faint_mag_limit(self, mag):
        self.port.write(':MS#')
        response = self.port.readline()
        return response
    # :SfsMM.M#
    # Set faint magnitude limit to sMM.M Returns:
    # 0 – Invalid 1 - Valid
    
    def set_id_field_diam(self, mm):
        self.port.write(':MS#')
        response = self.port.readline()
        return response
    # :SFNNN#
    # Set FIELD/IDENTIFY field diamter to NNNN arc minutes.
    # Returns:
    # 0 – Invalid
    # 1 - Valid
    
    def set_site_long(self, ddd, mm):
        self.port.write(':MS#')
        response = self.port.readline()
        return response
    # :SgDDD*MM#
    # Set current site’s longitude to DDD*MM an ASCII position string
    # Returns:
    # 0 – Invalid
    # 1 - Valid 
    
    def set_utc_offset(self, offset):
        self.port.write(':MS#')
        response = self.port.readline()
        return response
    # :SGsHH.H#
    # Set the number of hours added to local time to yield UTC Returns:
    # 0 – Invalid 1 - Valid
    
    def set_elev_limit_min(self, dd):
        self.port.write(':MS#')
        response = self.port.readline()
        return response
    # :ShDD#
    # Set the minimum object elevation limit to DD# Returns:
    # 0 – Invalid 1 - Valid
    
    def set_size_limit_min(self, mm):
        self.port.write(':MS#')
        response = self.port.readline()
        return response
    # :SlNNN#
    # Set the size of the smallest object returned by FIND/BROWSE to NNNN arc minutes Returns:
    # 0 – Invalid 1 - Valid
    
    def set_local_time(self, hh, mm, ss):
        self.port.write(':MS#')
        response = self.port.readline()
        return response
    # :SLHH:MM:SS#
    # Set the local Time
    # Returns:
    # 0 – Invalid
    # 1 - Valid
    
    def set_site_name(self, id, name):
        assert id in range(1,5)
        if id == 1:
            self.port.write(':SM{:15s}#')
        if id == 2:
            self.port.write(':SN{:15s}#')
        if id == 3:
            self.port.write(':SO{:15s}#')
        if id == 4:
            self.port.write(':SP{:15s}#')
        response = self.port.readline()
        return response
    # :SM<string>#
    # :SN<string>#
    # :SO<string>#
    # :SP<string>#
    # Set site n’s name to be <string>. LX200s only accept 3 character strings. Other scopes accept up to 15 characters. Returns:
    # 0 – Invalid 1 - Valid
    
    def set_elev_limit_max(self, dd):
        self.port.write(':MS#')
        response = self.port.readline()
        return response
    # :SoDD*#
    # Set highest elevation to which the telescope will slew Returns:
    # 0 – Invalid 1 - Valid
    
    def cycle_quality_limit(self):
        self.port.write(':MS#')
        response = self.port.readline()
        return response
    # :Sq#
    # Step the quality of limit used in FIND/BROWSE through its cycle of VP ... SU. Current setting can be queried with :Gq# Returns: Nothing
    
    def set_target_ra(self, hh, mm, ss):
        self.port.write(':MS#')
        response = self.port.readline()
        return response
    # :SrHH:MM.T# :SrHH:MM:SS#
    # Set target object RA to HH:MM.T or HH:MM:SS depending on the current precision setting. Returns:
    # 0 – Invalid 1 - Valid
    
    def set_size_limit_max(self, mm):
        self.port.write(':MS#')
        response = self.port.readline()
        return response
    # :SsNNN#
    # Set the size of the largest object the FIND/BROWSE command will return to NNNN arc minutes Returns:
    # 0 – Invalid 1 - Valid
    
    def set_lst(self, hh, mm, ss):
        self.port.write(':MS#')
        response = self.port.readline()
        return response
    # :SSHH:MM:SS#
    # Sets the local sideral time to HH:MM:SS Returns:
    # 0 – Invalid 1 - Valid
    
    def set_site_lat(self, dd, mm):
        self.port.write(':MS#')
        response = self.port.readline()
        return response
    # :StsDD*MM#
    # Sets the current site latitdue to sDD*MM# Returns:
    # 0 – Invalid 1 - Valid
    
    def set_tracking_rate(self, rate):
        assert rate > 0.0
        self.port.write(':MS#')
        response = self.port.readline()
        return response
    # :STTT.T#
    # Sets the current tracking rate to TTT.T hertz, assuming a model where a 60.0 Hertz synchronous motor will cause the RA axis to make exactly one revolution in 24 hours.
    # Returns:
    # 0 – Invalid 1 - Valid
    
    def set_slew_rate_max(self, rate):
        assert rate in range(2,9)
        self.port.write(':MS#')
        response = self.port.readline()
        return response
    # :SwN#
    # Set maximum slew rate to N degrees per second. N is the range (2..8) Returns: 0 – Invalid 1 - Valid
    
    def set_obj_sel_string(self, value):
        assert value in ['G', 'P', 'D', 'C', 'O']
        self.port.write(':MS#')
        response = self.port.readline()
        return response
    # :SyGPDCO#
    # Sets the object selection string used by the FIND/BROWSE command. Returns:
    # 0 – Invalid 1 - Valid
    
    def set_target_az(self, ddd, mm):
        self.port.write(':MS#')
        response = self.port.readline()
        return response
    # :SzDDD*MM#
    # Sets the target Object Azimuth [LX 16” and LX200GPS only] Returns:
    # 0 – Invalid 1 - Valid
    
    
    # T – Tracking Commands
    def tracking_increase(self):
        self.port.write(':T+#')
        response = self.port.readline()
        return response
    # :T+# Increment Manual rate by 0.1 Hz Returns: Nothing
    
    def tracking_decrease(self):
        self.port.write(':T-#')
        response = self.port.readline()
        return response
    # :T-# Decrement Manual rate by 0.1 Hz Returns: Nothing
    
    def tracking_lunar(self):
        self.port.write(':TL#')
        response = self.port.readline()
        return response
    # :TL# Set Lunar Tracking Rage Returns: Nothing
    
    def tracking_custom(self):
        self.port.write(':TM#')
        response = self.port.readline()
        return response
    # :TM# Select custom tracking rate Returns: Nothing
    
    def tracking_default(self):
        self.port.write(':TQ#')
        response = self.port.readline()
        return response
    # :TQ# Select default tracking rate Returns: Nothing
    
    def tracking_manual(self, rate):
        assert rate > 0.0
        self.port.write(':T{:07.3f}#'.format(rate))
        response = self.port.readline()
        return response
    # :TDDD.DDD# Set Manual rate to the ASCII expressed decimal DDD.DD Returns: ‘1’


    # U - Precision Toggle
    def toggle_precision(self):
        self.port.write(':U#')
        response = self.port.readline()
        return response
    # :U# Toggle between low/hi precision positions
    # Low - RA displays and messages HH:MM.T sDD*MM
    # High - Dec/Az/El displays and messages HH:MM:SS sDD*MM:SS 
    # Returns Nothing


    # W – Site Select
    def site_select(self, n):
        assert n in range(4)
        self.port.write(':W{:1d}#'.format(n)) 
        response = self.port.readline()
        return response
    # :W<n># Set current site to <n>, an ASCII digit in the range 0..3 Returns: Nothing


    # ? – Help Text Retrieval
    def help_start(self):
        self.port.write(':??#')
        response = self.port.readline()
        return response
    # :??# Set help text cursor to the start of the first line. Returns: <string>#
    # The <string> contains first string of the general handbox help file.
    
    def help_next(self):
        self.port.write(':?+#')
        response = self.port.readline()
        return response
    # :?+# Retrieve the next line of help text Returns: <string>#
    # The <string> contains the next string of general handbox help file
    
    def help_prev(self):
        self.port.write(':?-#')
        response = self.port.readline()
        return response
    # :?-# Retreive previos line of the handbox help text file. Returns: <string>#
    # The <string> contains the next string of general handbox help file

def main():
    pass

if __name__ == '__main__':
    main()

