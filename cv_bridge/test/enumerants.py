# Copyright (c) 2018 Intel Corporation.
# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest
import cv2
from cv_bridge import CvBridge, CvBridgeError, getCvType
import sensor_msgs.msg


class TestEnumerants(unittest.TestCase):

    def test_enumerants_cv2(self):
        img_msg = sensor_msgs.msg.Image()
        img_msg.width = 640
        img_msg.height = 480
        img_msg.encoding = 'rgba8'
        img_msg.step = 640 * 4
        img_msg.data = ((640 * 480) * '1234').encode()

        bridge_ = CvBridge()
        cvim = bridge_.imgmsg_to_cv2(img_msg, 'rgb8')

        import sys
        self.assertTrue(sys.getrefcount(cvim) == 2)

        # A 3 channel image cannot be sent as an rgba8
        self.assertRaises(CvBridgeError, lambda: bridge_.cv2_to_imgmsg(cvim, 'rgba8'))

        # but it can be sent as rgb8 and bgr8
        bridge_.cv2_to_imgmsg(cvim, 'rgb8')
        bridge_.cv2_to_imgmsg(cvim, 'bgr8')

        self.assertFalse(getCvType('32FC4') == cv2.CV_8UC4)
        self.assertTrue(getCvType('8UC1') == cv2.CV_8UC1)
        self.assertTrue(getCvType('8U') == cv2.CV_8UC1)

    def test_numpy_types(self):
        bridge_ = CvBridge()
        self.assertRaises(TypeError, lambda: bridge_.cv2_to_imgmsg(1, 'rgba8'))
        if hasattr(cv2, 'cv'):
            self.assertRaises(TypeError, lambda: bridge_.cv2_to_imgmsg(cv2.cv(), 'rgba8'))


if __name__ == '__main__':

    suite = unittest.TestSuite()
    suite.addTest(TestEnumerants('test_enumerants_cv2'))
    suite.addTest(TestEnumerants('test_numpy_types'))
    unittest.TextTestRunner(verbosity=2).run(suite)
