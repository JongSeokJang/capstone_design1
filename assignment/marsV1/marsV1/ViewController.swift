//
//  ViewController.swift
//  marsV1
//
//  Created by 이상협 on 2018. 5. 17..
//  Copyright © 2018년 이상협. All rights reserved.
//

import UIKit

struct SolarPanelsDataSource {
    let values = [1,1.5,2,2.5,3,3.5,4,4.5,5]
    
    func title(for index: Int) -> String? {
        guard index < values.count else {return nil}
        return String(values[index])
    }
    
    func values(for index: Int) -> Double? {
        guard index < values.count else {return nil}
        return Double(values[index])
    }
}

struct GreenHouseDataSource {
    let values = [1,2,3,4,5]
    
    func title(for index: Int) -> String? {
        guard index < values.count else {return nil}
        return String(values[index])
    }
    
    func values(for index: Int) -> Double? {
        guard index < values.count else {return nil}
        return Double(values[index])
    }
}

struct SizeDataSource {
    
    private static let numberFormatter: NumberFormatter = {
        let formatter = NumberFormatter()
        formatter.locale = .current
        formatter.numberStyle = .decimal
        formatter.usesGroupingSeparator = true
        return formatter
        
    }()
    
    let values = [
        750,
        1000,
        1500,
        2000,
        3000,
        4000,
        5000,
        10_000
    ]
    
    func title(for index: Int) -> String? {
        guard index < values.count else {return nil}
        return String(values[index])
    }
    
    func values(for index: Int) -> Double? {
        guard index < values.count else {return nil}
        return Double(values[index])
    }
}

enum Feature: Int {
    case solarPanels = 0, greenHouse, Acres }


class ViewController: UIViewController, UIPickerViewDelegate, UIPickerViewDataSource {
    
    let model = marshabitatpricer()

   // let pickerDatasource = PickerDataSource()

    
    @IBOutlet weak var priceLabel: UILabel!
    @IBOutlet weak var pickerView: UIPickerView! //{
       // didSet {
//            pickerView.delegate = self
//
//            pickerView.dataSource = pickerDatasource
//
//            let features: [Feature] = [.solarPanels, .greenHouse, .Acres]
//
//            for feature in features {
//                pickerView.selectRow(2, inComponent: feature.rawValue, animated: false)
//                print("feature.rawValue = ", feature.rawValue)
//            }
       // }
  //  }
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    func pickerView(_ pickerView: UIPickerView, didSelectRow row: Int, inComponent component: Int) {
        print("Selected Row = ",row)
        
       // updatedPredictPrice()
    }
    
    func pickerView(_ pickerView: UIPickerView, titleForRow row: Int, forComponent component: Int) -> String? {
        guard let feature = Feature(rawValue: component) else {
            fatalError("component \(component) found to represent a \(Feature.self). This should not based on the configuration set in the storyboard.")
        }
        
        return self.title(for: row, feature: feature)
    }

//    func updatedPredictPrice() {
//        func selectedRow(for feature: Feature) -> Int {
//            return pickerView.selectedRow(inComponent: feature.rawValue)
//        }
//
//        let solarPanels = self.value(for: selectedRow(for: .solarPanels), feature: .solarPanels)
//        let greenHouse  = self.value(for: selectedRow(for: .greenHouse), feature: .greenHouse)
//        let size = self.value(for: selectedRow(for: .Acres), feature: .Acres)
//
//        print("solarPanels = ",solarPanels,greenHouse,size)
//
//        guard let marsHabitatPricerOutput = try? model.prediction(solarPanels: solarPanels, greenhouses:  greenHouse, size: size) else {
//            fatalError("Unexpected runtime error.")
//        }
//
//        let price = marsHabitatPricerOutput.price
//        priceLabel.text = priceFormatter.string(for: price)
//    }

    func numberOfComponents(in pickerView: UIPickerView) -> Int {
        return 3
    }
    
    func pickerView(_ pickerView: UIPickerView, numberOfRowsInComponent component: Int) -> Int {
        switch Feature (rawValue: component)! {
        case .solarPanels: return solarPanelsDataSource.values.count
            
        case .greenHouse: return greenHouseDataSource.values.count
            
        case .Acres: return sizeDataSource.values.count
        }
    }
    
    
    private let solarPanelsDataSource = SolarPanelsDataSource()
    private let greenHouseDataSource = GreenHouseDataSource()
    private let sizeDataSource = SizeDataSource()
    
    func title (for row: Int, feature: Feature) -> String? {
        switch feature {
        case .solarPanels:
            return solarPanelsDataSource.title(for: row)
        case .greenHouse:
            return greenHouseDataSource.title(for: row)
        case .Acres:
            return sizeDataSource.title(for: row)
        }
    }
    
    func value(for row: Int, feature: Feature) -> Double {
        let value: Double?
        
        switch feature {
        case .solarPanels:
            value = solarPanelsDataSource.values(for: row)
        case .greenHouse:
            value = greenHouseDataSource.values(for: row)
        case .Acres:
            value = sizeDataSource.values(for: row)
            
        }
        return value!
        
    }
}


