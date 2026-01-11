to activate venv: .\\venv\\Scripts\\activate

2\. Which EXIF fields are modified or added



Metadata-based steganography does not touch core camera fields.

Instead, it targets text-capable, optional fields, for example:



Field			Action

UserComment		Value modified / inserted

ImageDescription	Value modified

Artist			Value modified

Copyright		Value modified

XMP custom fields	Added

Padding or unused tags	can be modified



========================================================================================================

Camera and capture fields

(ExposureTime, ISO, FNumber, FocalLength, etc.)



Geometry and rendering fields

(ImageWidth, ImageLength, Orientation)



Color and pixel description fields

(ColorSpace, BitsPerSample)



These are core, camera-generated fields and they remain unchanged.

format of exif(metadata)

Tag ID: 0x010F

Tag Name: Make

Data Type: ASCII



\[ Header / Metadata ]  → descriptive information

\[ Image Data ]         → actual pixels (colors, intensity)



Image width and height



Color depth (8-bit, 24-bit, etc.)

Compression method

Color space (RGB, CMYK)

Creation date and time

Camera or software used

Author, copyright, description

Orientation, DPI, GPS data

**All of this is called metadata**

**So inside the image header, it looks like:**



**Tag: ImageDescription**

**Value: 44 65 6D 6F 20 54 65 78 74**



**Header Text (Metadata)		Pixel-based Steganography**

Stored before image data	Stored inside pixel values

Easy to view with tools		Difficult to detect

Not part of image content	Alters pixel bits slightly

Used for information		Used for secrecy



5\. Why metadata-based steganography is used

**Advantages**

Very easy to implement

No image distortion

Large metadata fields allow long messages

No advanced signal processing required



**Common use cases**

Covert labeling

Watermarking

Proof of ownership

Simple data hiding for assignments or demos



6\. Limitations and weaknesses



Metadata-based steganography is not secure against informed analysis.



Major weaknesses:

Metadata is easy to inspect

Many platforms strip metadata automatically

Re-saving or editing images often deletes metadata

Forensic tools flag unusual metadata sizes



**Tools used to detect exif steganography**:

exiftool

strings

forensic image parsers



What DOES change when encrypted text is added to metadata



Although visual specifications remain the same, file-level characteristics change.



**Changes that occur**:



Metadata size increases

EXIF/XMP/IPTC sections grow

Overall file size increases slightly

Metadata checksum / offsets update

New or modified metadata tags appear



Image Type			EXIF Present	has\_exif

Screenshot			No		False

Downloaded social media image	No		False

Camera photo			Yes		True

Image with metadata stego	Yes (added)	True

