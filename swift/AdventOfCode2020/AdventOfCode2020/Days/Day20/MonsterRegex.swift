//
//  MonsterRegex.swift
//  AdventOfCode2020
//
//  Created by gary on 25/12/2020.
//

import Foundation

final class MonsterRegex {
    private let parts = [
        "..................#.",
        "#....##....##....###",
        ".#..#..#..#..#..#..."
    ]

    let size = 15

    init() {}


    func count(in string: String) -> Int {
        let imageWidth = Int(Double(string.count).squareRoot())
        assert(imageWidth * imageWidth == string.count)
        let spacerWidth = imageWidth - parts[0].count
        let spacer = Array(repeating: ".", count: spacerWidth).joined()
        let pattern = parts.joined(separator: spacer)
        let re = try! NSRegularExpression(pattern: pattern, options: [])
        var rangeStart = 0
        var matchCount = 0
        while true {
            let range = NSRange(location: rangeStart, length: string.count - rangeStart)
            guard let m = re.firstMatch(in: string, options: [], range: range) else {
                break
            }
            matchCount += 1
            rangeStart = m.range.lowerBound + 1
        }
        return matchCount
    }
}
