//
//  ChecklistItem.swift
//  check_list2
//
//  Created by Jongseok Jang on 2018. 5. 30..
//  Copyright © 2018년 Jongseok Jang. All rights reserved.
//

import Foundation

class ChecklistItem {
    var text=""
    var checked = false
    
    /* For toggling */
    func toggleChecked() {
        checked = !checked
    }
    
}
