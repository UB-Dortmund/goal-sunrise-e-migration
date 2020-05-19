from xml.etree import ElementTree


def xml_splitter(source_dir='', filename='', namespace='marc', target_dir='', size=500):

    ElementTree.register_namespace(namespace, 'http://www.loc.gov/MARC21/slim')

    context = ElementTree.iterparse('%s/%s' % (source_dir, filename), events=('end',))

    cnt_records = 0
    cnt_files = 0
    xml_data = ''

    header = '<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<%s:collection xmlns:%s="http://www.loc.gov/MARC21/slim" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.loc.gov/MARC21/slim http://www.loc.gov/standards/marcxml/schema/MARC21slim.xsd">\n' % (
    namespace, namespace)
    footer = "</%s:collection>" % namespace

    for event, elem in context:

        if elem.tag == '{http://www.loc.gov/MARC21/slim}record':
            cnt_records += 1
            xml_data += '%s\n' % ElementTree.tostring(elem).decode('utf-8')

            if cnt_records == size:
                cnt_files += 1
                with open('%s/%s.%s.xml' % (target_dir, filename.replace('.xml', ''), cnt_files), 'wb') as f:
                    f.write(header.encode('utf-8'))
                    f.write(xml_data.encode('utf-8'))
                    f.write(footer.encode('utf-8'))

                cnt_records = 0
                xml_data = ''

    cnt_files += 1

    with open('%s/%s.%s.xml' % (target_dir, filename.replace('.xml', ''), cnt_files), 'wb') as f:
        f.write(header.encode('utf-8'))
        f.write(xml_data.encode('utf-8'))
        f.write(footer.encode('utf-8'))


if __name__ == '__main__':

    xml_splitter(source_dir='/home/mhagbeck/data/GOAL/SunRiseMARCXML', filename='807g_alleGOAL.TIT',
                 namespace='mx',
                 target_dir='/home/mhagbeck/data/GOAL/807gAlle', size=5000)
