//
//  ViewController.swift
//  MarV1
//
//  Created by Jongseok Jang on 2018. 5. 21..
//  Copyright © 2018년 Jongseok Jang. All rights reserved.
//

import UIKit

enum Feature: Int {
    case solarPanels = 0, greenhouses, size }


class ViewController: UIViewController, UIPickerViewDelegate{

    
    let pickerDataSource = PickerDataSource()
    @IBOutlet weak var pickerView: UIPickerView!{
        didSet {
            pickerView.delegate = self
            
            pickerView.dataSource =
        }
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }


}

