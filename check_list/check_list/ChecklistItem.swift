//
//  ChecklistItem.swift
//  CheckListsV3
//
//  Created by Myoung-Wan Koo on 2018. 5. 30..
//  Copyright © 2018년 Myoung-Wan Koo. All rights reserved.
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
