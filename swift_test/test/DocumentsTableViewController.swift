//
//  DocumentsTableViewController.swift
//  test
//
//  Created by Keshav Maheshwari on 4/2/20.
//  Copyright © 2020 Masayoshi Iwasa. All rights reserved.
//

import Foundation
import UIKit

class DocumentsTableViewController: UIViewController, UITableViewDelegate, UITableViewDataSource {
    
    let documents: [String] = ["Application for Criminal Complaint (Court)", "Application for Criminal Complaint (Justice Department)", "Police Department Arrest Booking Form", "Arrest Report", "Offense/Incident Report", "Supplemental Report", "Criminal Complaint", "Incident Report", "Court Activity Record Information"]
    
    
    
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        <#code#>
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        <#code#>
    }
    
    
    
}
